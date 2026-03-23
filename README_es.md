# NihongoPy

<p align="center">
  <img src="nihongopy_logo.png" alt="Logo de NihongoPy" width="220">
</p>

NihongoPy es una aplicación de terminal para practicar japonés de forma sencilla, rápida y sin castigos absurdos.

Nace como una alternativa gratuita a esas apps de idiomas que, en cuanto fallas una respuesta, parece que te quieren expulsar del sistema educativo. Aquí no. Aquí fallas, ves la corrección, aprendes algo y sigues adelante como una persona normal.

## Qué es

Un entrenador de japonés en terminal centrado en practicar y repasar:

- `Hiragana`
- `Katakana`
- `Kanji`
- `Gramática`

También incluye modo de `repaso`, interfaz en `español` e `inglés` y una experiencia muy ligera, sin registros, sin anuncios y sin rachas amenazantes mirándote desde una esquina.

## Por qué existe

Porque a veces solo quieres aprender.

Sin vidas limitadas.
Sin bloqueos artificiales.
Sin que una app te haga sentir que has decepcionado a tu linaje por confundir `shi` con `chi`.

NihongoPy está pensado para practicar, equivocarte, entender el error y continuar.

## Características

- Modo de práctica para `Hiragana`, `Katakana`, `Kanji` y `Gramática`
- Modo de repaso para consultar tablas de kana y listas de kanji
- Interfaz multidioma en español e inglés
- Feedback inmediato al fallar
- Explicaciones rápidas dentro del flujo
- Aplicación 100% terminal

## Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/marcalcaina/nihongopy.git
cd nihongopy
```

2. Crea un entorno virtual:

```bash
python -m venv .venv
```

3. Actívalo:

En Windows:

```bash
.venv\Scripts\activate
```

En macOS o Linux:

```bash
source .venv/bin/activate
```

4. Instala las dependencias:

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
python main.py
```

## Dependencias

Este proyecto utiliza:

- `rich`
- `questionary`

Todas están incluidas en `requirements.txt`.

## Estructura del proyecto

- `main.py`: aplicación principal
- `interface.json`: textos de interfaz y literales multidioma
- `hiragana.json`: datos de hiragana
- `katakana.json`: datos de katakana
- `kanji.json`: datos de kanji
- `grammar.json`: ejercicios de gramática

## Estado actual del proyecto

- Gratis
- Hecho para terminal
- Rápido de usar
- Bastante simpático
- Sorprendentemente útil

## Contribuciones

Si quieres mejorar el contenido, añadir más niveles de JLPT, ampliar vocabulario, pulir la interfaz o hacer el proyecto todavía más divertido, las contribuciones son bienvenidas.

## Licencia

Úsalo, modifícalo, aprende con él y hazlo mejor.
