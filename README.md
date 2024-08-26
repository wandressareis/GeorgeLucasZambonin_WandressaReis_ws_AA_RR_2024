## Análise do Algoritmo "VerificaAlgo"

### Função de custo T(n)

#### Resolução:

#### Disponível no slide

<img src="readme_assets/resolucao_slide.png" width="350" height="400" alt="Descrição da imagem">

##### Resolução com passo a passo do slide
<img src="readme_assets/passo-a-passo_com_slide.jpg" width="300" height="400" alt="Descrição da imagem">

<img src="readme_assets/continuacao.jpg" width="300" height="70" alt="Descrição da imagem">

#### Função de custo correta
![alt text](./readme_assets/funcao_de_custo.png)

#### Comparação T(n)
#### T(n) slide:
$$
T(n) = 10000n^2 - 50000n
$$

#### T(n) atual:

$$
T(n) = \frac{n \cdot \left( \min\left(n - 5, \left\lfloor \frac{n}{2} \right\rfloor - 1\right)\right) \cdot \left( \min\left(n - 5, \left\lfloor \frac{n}{2} \right\rfloor - 2\right)\right)}{2}
$$


![alt text](assets/graphs/func_custo_t.png)

### Complexidade

![alt text](assets/graphs/complexity_time.png)

### Projeção assintotica $O(n^3)$

![alt text](assets/graphs/actual_t_projection.png)

## Requirements

- GIT
- Python > 3.10

## Usage

### linux

#### Run on terminal:
```bash
git clone https://github.com/wandressareis/GeorgeLucasZambonin_WandressaReis_ws_AA_RR_2024
cd GeorgeLucasZambonin_WandressaReis_ws_AA_RR_2024
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 ./app.py
```