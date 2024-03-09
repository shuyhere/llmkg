# llmkg

## Convert any Corpus of Text into a *Graph of Knowledge*

see [guide](./knowledge_graph/README.md)



## optional:use conda as poetry as package manager

```bash
conda create -n my_project_env python=3.10
conda activate my_project_env
```
```bash
conda install
```
Navigate to your project directory and run:
```bash
poetry init
```
```bash
poetry add pandas numpy matplotlib
```
```bash
poetry lock
```
```bash
conda env export | grep -v "^prefix: " > environment.yml
```
```bash
conda env create -f environment.yml
poetry install
```
