# PROGRESS-BAR

## information

Progress-bar est un module python qui permet de créer des barres de progression à intergré dans tout type de projet.

## création d'une barre de progression

```python
from progress_bar import Bar

objet = Bar(steps, char, mode)

# exemple
objet = Bar(10, '*', 'p')
```

## mise en fonctionnement

```python
for step in range(10)
    bar.progress(step + 1)
    sleep(0.1)
```

## modes

| mode | description |
| ---- | ----------- |
| p    | percents    |
| s    | step        |
| c    | clean       |