#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <cmath>
#include <random>
#include <climits>
#include <vector>
#include <algorithm>

using namespace std;

typedef struct {
    double x, y;
} Point;

typedef struct {
    Point a, b;
} Segment;

typedef struct No {
    struct No *esq;
    struct No *dir;
    struct No *pai;
    Point p;
    int id;
} No;

typedef No* ptrNo;

typedef struct Candidato{
    ptrNo no;
    double custo;

    bool operator<(const Candidato& outro) const {
        return custo < outro.custo;
    }
} Candidato;

double distancia(Point P, Point Q){
    return sqrt(pow((Q.x - P.x), 2) + pow((Q.y - P.y), 2));
}

double gerarDoubleAleatorio(double raio, mt19937 &gen){
    uniform_real_distribution<double> dis(-raio, raio);
    return dis(gen);
}

Point gerarPontoAleatorio(double raio, mt19937 &gen){
    double x, y;
    x = gerarDoubleAleatorio(raio, gen);
    y = gerarDoubleAleatorio(raio, gen);
    if(x*x + y*y <= raio*raio){
        Point P;
        P.x = x; P.y = y;
        return P;
    }else {
        return gerarPontoAleatorio(raio, gen);
    }
}

ptrNo criarNo(Point P, int id, ptrNo pai){
    ptrNo novo = (ptrNo) malloc(sizeof(No));

    if(novo == NULL){
        cout << "Erro ao alocar memória para o novo nó" << endl;
        return NULL;
    }

    novo->p = P;
    novo->id = id;
    novo->pai = pai;
    novo->esq = NULL;
    novo->dir = NULL;

    return novo;
}

void gerarCandidatos(Point novo, ptrNo raiz, vector<Candidato>& candidatos){
    if (raiz == NULL){
        return;
    }
    if (raiz->dir == NULL || raiz->esq == NULL){
        Candidato candidato;
        candidato.no = raiz;
        candidato.custo = distancia(raiz->p, novo);
        candidatos.push_back(candidato);
    }
    gerarCandidatos(novo, raiz->esq, candidatos);
    gerarCandidatos(novo, raiz->dir, candidatos);
}

void inserirNo(Point novo, ptrNo pai, int id){
    ptrNo novoNo = criarNo(novo, id, pai);
    if (pai->dir == NULL){
        pai->dir = novoNo;
    } else {
        pai->esq = novoNo;
    }
}

int main(int argc, char *argv[]){
    int Nterm;
    double raio;

    if (argc != 3) {
        cout << "Uso: " << argv[0] << " Nterm Raio" << endl;
        exit(1);
    }

    Nterm = atoi(argv[1]); raio = atof(argv[2]);
    cout << "Nterm = " << Nterm << endl;
    cout << "Raio = " << raio << endl;

    Point centro; 
    centro.x = 0.0; centro.y = 0.0;
    ptrNo raiz = criarNo(centro, 0, NULL);

    random_device rd;
    mt19937 gen(rd());
    for (int i = 1; i <= Nterm; i++){
        Point P = gerarPontoAleatorio(raio, gen);

        vector<Candidato> candidatos;
        gerarCandidatos(P, raiz, candidatos);

        sort(candidatos.begin(), candidatos.end());

        Candidato melhor = candidatos[0];

        inserirNo(P, melhor.no, i);
    }

    return 0;
}