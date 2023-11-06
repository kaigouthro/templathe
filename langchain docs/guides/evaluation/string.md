# String Evaluators

A string evaluator is a component within LangChain designed to assess the performance of a language model by comparing its generated outputs (predictions) to a reference string or an input. This comparison is a crucial step in the evaluation of language models, providing a measure of the accuracy or quality of the generated text.

In practice, string evaluators are typically used to evaluate a predicted string against a given input, such as a question or a prompt. Often, a reference label or context string is provided to define what a correct or ideal response would look like. These evaluators can be customized to tailor the evaluation process to fit your application's specific requirements.

To create a custom string evaluator, inherit from the `StringEvaluator` class and implement the `_evaluate_strings` method. If you require asynchronous support, also implement the `_aevaluate_strings` method.

Here's a summary of the key attributes and methods associated with a string evaluator:

- `evaluation_name`: Specifies the name of the evaluation.
- `requires_input`: Boolean attribute that indicates whether the evaluator requires an input string. If True, the evaluator will raise an error when the input isn't provided. If False, a warning will be logged if an input *is* provided, indicating that it will not be considered in the evaluation.
- `requires_reference`: Boolean attribute specifying whether the evaluator requires a reference label. If True, the evaluator will raise an error when the reference isn't provided. If False, a warning will be logged if a reference *is* provided, indicating that it will not be considered in the evaluation.

String evaluators also implement the following methods:

- `aevaluate_strings`: Asynchronously evaluates the output of the Chain or Language Model, with support for optional input and label.
- `evaluate_strings`: Synchronously evaluates the output of the Chain or Language Model, with support for optional input and label.

The following sections provide detailed information on available string evaluator implementations as well as how to create a custom string evaluator.

## 📄️ Criteria Evaluation

Open In Colab

## 📄️ Custom String Evaluator

Open In Colab

## 📄️ Embedding Distance

Open In Colab

## 📄️ Exact Match

Open In Colab

## 📄️ Regex Match

Open In Colab

## 📄️ Scoring Evaluator

The Scoring Evaluator instructs a language model to assess your model's predictions on a specified scale (default is 1-10) based on your custom criteria or rubric. This feature provides a nuanced evaluation instead of a simplistic binary score, aiding in evaluating models against tailored rubrics and comparing model performance on specific tasks.

## 📄️ String Distance

Open In Colab
