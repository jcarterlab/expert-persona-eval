# 🧪 Expert Persona Eval

An evaluation testing whether prompting an LLM with an expert persona improves accuracy on reasoning tasks.

The experiment compares two conditions, a control condition with no persona and an experimental condition with an expert persona, on the same set of 500 randomly selected questions from the MMLU-Pro dataset. Both conditions use the gemini-2.5-flash-lite model at temperature 0 to minimise randomness, isolating the effect of the persona itself. The results are analysed using bootstrapping to estimate uncertainty around the observed effect size and the Exact McNemar's test to assess statistical significance. It finds a lack of evidence for expert persona efficacy.

**Key technologies:** Python, Jupyter, Pandas, NumPy, Google Gemini API, Matplotlib.

## 🔍 Overview

This evaluation involves the following steps: 

1. Design
2. Data collection
3. Data analysis
4. Interpretation

## 📐 Design

The evaluation was built around the following core elements:

| Element | Details |
|---|---|
| **Conditions** | No persona (control) · Expert persona (experimental) |
| **Dataset** | MMLU-Pro — 500 randomly selected questions |
| **Model(s)** | gemini-2.5-flash-lite |
| **LLM settings** | Temperature: 0 |
| **Evaluation** | Bootstrapping · Exact McNemar's test |

## 🛢️ Data collection

## 📊 Data analysis

## 💡Interpretation

