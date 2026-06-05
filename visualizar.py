import csv
import math
import random

import numpy as np
import pandas as pd
import pyvista as pv


def gerar_segmentos(quantidade, raio=100.0, arquivo="segmentos.csv"):
    nodes = [(0.0, 0.0)]
    children = {0: 0}
    segments = []

    for _ in range(quantidade):
        while True:
            x = random.uniform(-raio, raio)
            y = random.uniform(-raio, raio)
            if x * x + y * y <= raio * raio:
                break

        candidates = [i for i in range(len(nodes)) if children.get(i, 0) < 2]
        parent = min(candidates, key=lambda i: math.dist(nodes[i], (x, y)))
        x1, y1 = nodes[parent]

        segments.append((x1, y1, x, y))
        nodes.append((x, y))
        children[parent] = children.get(parent, 0) + 1
        children[len(nodes) - 1] = 0

    with open(arquivo, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["x1", "y1", "x2", "y2"])
        writer.writerows(segments)

    print(f"Gerados {len(segments)} segmentos em {arquivo}.")
    print(f"Total de pontos incluindo a raiz: {len(nodes)}")


def visualizar(arquivo="segmentos.csv"):
    dados = pd.read_csv(arquivo)

    points = []
    point_map = {}
    lines = []

    for _, row in dados.iterrows():
        p1 = (row.x1, row.y1, 0)
        p2 = (row.x2, row.y2, 0)

        if p1 not in point_map:
            point_map[p1] = len(points)
            points.append(p1)

        if p2 not in point_map:
            point_map[p2] = len(points)
            points.append(p2)

        i = point_map[p1]
        j = point_map[p2]
        lines.extend([2, i, j])

    mesh = pv.PolyData()
    mesh.points = np.array(points)
    mesh.lines = np.array(lines)

    plotter = pv.Plotter()
    plotter.add_mesh(mesh, color="red", line_width=3)
    plotter.add_points(mesh.points, color="black", point_size=8, render_points_as_spheres=True)
    plotter.show()


def pedir_quantidade():
    while True:
        print("\nEscolha a quantidade de segmentos:")
        print("1 - 10 segmentos")
        print("2 - 50 segmentos")
        print("3 - 100 segmentos")
        print("4 - Digitar outro valor")
        print("0 - Sair")

        opcao = input("Opcao: ").strip()

        if opcao == "0":
            return None
        if opcao == "1":
            return 10
        if opcao == "2":
            return 50
        if opcao == "3":
            return 100
        if opcao == "4":
            valor = input("Digite a quantidade de segmentos: ").strip()
            if valor.isdigit() and int(valor) > 0:
                return int(valor)
            print("Digite um numero inteiro maior que zero.")
            continue

        print("Opcao invalida.")


def main():
    while True:
        quantidade = pedir_quantidade()
        if quantidade is None:
            break

        gerar_segmentos(quantidade)
        visualizar()

        repetir = input("\nDeseja testar outro valor? (s/n): ").strip().lower()
        if repetir != "s":
            break


if __name__ == "__main__":
    main()
