import pyvista as pv
import numpy as np
import sys

def carregar_arvore_csv(caminho_arquivo):
    """Lê o arquivo CSV gerado pelo C++ e retorna pontos e linhas no formato PyVista."""
    pontos_set = set()
    linhas = []
    
    with open(caminho_arquivo, 'r') as f:
        next(f)  # pula cabeçalho (se existir)
        for linha in f:
            if not linha.strip():
                continue
            x1, y1, x2, y2 = map(float, linha.strip().split(','))
            # Adiciona os dois pontos ao conjunto
            pontos_set.add((x1, y1, 0.0))
            pontos_set.add((x2, y2, 0.0))
            # Guarda a linha como par de índices (ainda não sabemos os índices)
            linhas.append(((x1, y1, 0.0), (x2, y2, 0.0)))
    
    # Cria um mapeamento ponto -> índice
    pontos_lista = list(pontos_set)
    ponto_para_idx = {p: i for i, p in enumerate(pontos_lista)}
    
    # Constrói o array de linhas no formato do PyVista:
    # [n_points, idx1, idx2, ...]
    linhas_pyvista = []
    for (p1, p2) in linhas:
        linhas_pyvista.append(2)               # número de pontos na linha
        linhas_pyvista.append(ponto_para_idx[p1])
        linhas_pyvista.append(ponto_para_idx[p2])
    
    return np.array(pontos_lista, dtype=np.float64), np.array(linhas_pyvista, dtype=np.int64)

def main():
    if len(sys.argv) != 2:
        print("Uso: python visualizar.py <arquivo.csv>")
        sys.exit(1)
    
    arquivo = sys.argv[1]
    pontos, linhas = carregar_arvore_csv(arquivo)
    
    mesh = pv.PolyData()
    mesh.points = pontos
    mesh.lines = linhas
    
    circle = pv.Circle(radius=10.0)  # use seu raio R

    plotter = pv.Plotter()
    plotter.add_mesh(mesh, line_width=3, color='blue')
    plotter.add_mesh(circle, color='red', line_width=1, style='wireframe')
    plotter.show()

if __name__ == "__main__":
    main()