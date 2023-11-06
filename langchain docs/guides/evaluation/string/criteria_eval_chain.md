# Criteria Evaluation

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/langchain-ai/langchain/blob/master/docs/docs/guides/evaluation/string/criteria_eval_chain.ipynb)

![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)

In scenarios where you wish to assess a model's output using a specific rubric or criteria set, the `criteria` evaluator proves to be a handy tool. It allows you to verify if an LLM or Chain's output complies with a defined set of criteria.

To understand its functionality and configurability in depth, refer to the reference documentation of the [CriteriaEvalChain](https://api.python.langchain.com/en/latest/evaluation/langchain.evaluation.criteria.eval_chain.CriteriaEvalChain.html#langchain.evaluation.criteria.eval_chain.CriteriaEvalChain) class.

### Usage without references[​](#usage-without-references "Direct link to Usage without references")

In this example, you will use the `CriteriaEvalChain` to check whether an output is concise. First, create the evaluation chain to predict whether outputs are "concise".

```python
from langchain.evaluation import load\_evaluator  
  
evaluator = load\_evaluator("criteria", criteria="conciseness")  
  
# This is equivalent to loading using the enum  
from langchain.evaluation import EvaluatorType  
  
evaluator = load\_evaluator(EvaluatorType.CRITERIA, criteria="conciseness")  

```

```python
eval\_result = evaluator.evaluate\_strings(  
 prediction="What's 2+2? That's an elementary question. The answer you're looking for is that two and two is four.",  
 input="What's 2+2?",  
)  
print(eval\_result)  

```

```text
 {'reasoning': 'The criterion is conciseness, which means the submission should be brief and to the point. \n\nLooking at the submission, the answer to the question "What\'s 2+2?" is indeed "four". However, the respondent has added extra information, stating "That\'s an elementary question." This statement does not contribute to answering the question and therefore makes the response less concise.\n\nTherefore, the submission does not meet the criterion of conciseness.\n\nN', 'value': 'N', 'score': 0}  

```

#### Output Format[​](#output-format "Direct link to Output Format")

All string evaluators expose an [evaluate_strings](https://api.python.langchain.com/en/latest/evaluation/langchain.evaluation.criteria.eval_chain.CriteriaEvalChain.html?highlight=evaluate_strings#langchain.evaluation.criteria.eval_chain.CriteriaEvalChain.evaluate_strings) (or async [aevaluate_strings](https://api.python.langchain.com/en/latest/evaluation/langchain.evaluation.criteria.eval_chain.CriteriaEvalChain.html?highlight=evaluate_strings#langchain.evaluation.criteria.eval_chain.CriteriaEvalChain.aevaluate_strings)) method, which accepts:

- input (str) – The input to the agent.
- prediction (str) – The predicted response.

The criteria evaluators return a dictionary with the following values:

- score: Binary integer 0 to 1, where 1 would mean that the output is compliant with the criteria, and 0 otherwise
- value: A "Y" or "N" corresponding to the score
- reasoning: String "chain of thought reasoning" from the LLM generated prior to creating the score

## Using Reference Labels[​](#using-reference-labels "Direct link to Using Reference Labels")

Some criteria (such as correctness) require reference labels to work correctly. To do this, initialize the `labeled_criteria` evaluator and call the evaluator with a `reference` string.

```python
evaluator = load\_evaluator("labeled\_criteria", criteria="correctness")  
  
# We can even override the model's learned knowledge using ground truth labels  
eval\_result = evaluator.evaluate\_strings(  
 input="What is the capital of the US?",  
 prediction="Topeka, KS",  
 reference="The capital of the US is Topeka, KS, where it permanently moved from Washington D.C. on May 16, 2023",  
)  
print(f'With ground truth: {eval\_result["score"]}')  

```

```text
 With ground truth: 1  

```

**Default Criteria**

Most of the time, you'll want to define your own custom criteria (see below), but we also provide some common criteria you can load with a single string.
Here's a list of pre-implemented criteria. Note that in the absence of labels, the LLM merely predicts what it thinks the best answer is and is not grounded in actual law or context.

```python
from langchain.evaluation import Criteria  
  
# For a list of other default supported criteria, try calling `supported\_default\_criteria`  
list(Criteria)  

```

```text
 [<Criteria.CONCISENESS: 'conciseness'>,  
 <Criteria.RELEVANCE: 'relevance'>,  
 <Criteria.CORRECTNESS: 'correctness'>,  
 <Criteria.COHERENCE: 'coherence'>,  
 <Criteria.HARMFULNESS: 'harmfulness'>,  
 <Criteria.MALICIOUSNESS: 'maliciousness'>,  
 <Criteria.HELPFULNESS: 'helpfulness'>,  
 <Criteria.CONTROVERSIALITY: 'controversiality'>,  
 <Criteria.MISOGYNY: 'misogyny'>,  
 <Criteria.CRIMINALITY: 'criminality'>,  
 <Criteria.INSENSITIVITY: 'insensitivity'>]  

```

## Custom Criteria[​](#custom-criteria "Direct link to Custom Criteria")

To evaluate outputs against your own custom criteria, or to be more explicit the definition of any of the default criteria, pass in a dictionary of `"criterion_name": "criterion_description"`

Note: it's recommended that you create a single evaluator per criterion. This way, separate feedback can be provided for each aspect. Additionally, if you provide antagonistic criteria, the evaluator won't be very useful, as it will be configured to predict compliance for ALL of the criteria provided.

```python
custom\_criterion = {"numeric": "Does the output contain numeric or mathematical information?"}  
  
eval\_chain = load\_evaluator(  
 EvaluatorType.CRITERIA,  
 criteria=custom\_criterion,  
)  
query = "Tell me a joke"  
prediction = "I ate some square pie but I don't know the square of pi."  
eval\_result = eval\_chain.evaluate\_strings(prediction=prediction, input=query)  
print(eval\_result)  
  
# If you wanted to specify multiple criteria. Generally not recommended  
custom\_criteria = {  
 "numeric": "Does the output contain numeric information?",  
 "mathematical": "Does the output contain mathematical information?",  
 "grammatical": "Is the output grammatically correct?",  
 "logical": "Is the output logical?",  
}  
  
eval\_chain = load\_evaluator(  
 EvaluatorType.CRITERIA,  
 criteria=custom\_criteria,  
)  
eval\_result = eval\_chain.evaluate\_strings(prediction=prediction, input=query)  
print("Multi-criteria evaluation")  
print(eval\_result)  

```

```text
 {'reasoning': "The criterion asks if the output contains numeric or mathematical information. The joke in the submission does contain mathematical information. It refers to the mathematical concept of squaring a number and also mentions 'pi', which is a mathematical constant. Therefore, the submission does meet the criterion.\n\nY", 'value': 'Y', 'score': 1}  
 {'reasoning': 'Let\'s assess the submission based on the given criteria:\n\n1. Numeric: The output does not contain any explicit numeric information. The word "square" and "pi" are mathematical terms but they are not numeric information per se.\n\n2. Mathematical: The output does contain mathematical information. The terms "square" and "pi" are mathematical terms. The joke is a play on the mathematical concept of squaring a number (in this case, pi).\n\n3. Grammatical: The output is grammatically correct. The sentence structure, punctuation, and word usage are all correct.\n\n4. Logical: The output is logical. It makes sense within the context of the joke. The joke is a play on words between the mathematical concept of squaring a number (pi) and eating a square pie.\n\nBased on the above analysis, the submission does not meet all the criteria because it does not contain numeric information.\nN', 'value': 'N', 'score': 0}  

```

## Using Constitutional Principles[​](#using-constitutional-principles "Direct link to Using Constitutional Principles")

Custom rubrics are similar to principles from [Constitutional AI](https://arxiv.org/abs/2212.08073). You can directly use your `ConstitutionalPrinciple` objects to
instantiate the chain and take advantage of the many existing principles in LangChain.

```python
from langchain.chains.constitutional\_ai.principles import PRINCIPLES  
  
print(f"{len(PRINCIPLES)} available principles")  
list(PRINCIPLES.items())[:5]  

```

```text
 54 available principles  
  
  
  
  
  
 [('harmful1',  
 ConstitutionalPrinciple(critique\_request='Identify specific ways in which the assistant’s last response is harmful, unethical, racist, sexist, toxic, dangerous, or illegal.', revision\_request='Please rewrite the assistant response to remove any and all harmful, unethical, racist, sexist, toxic, dangerous, or illegal content.', name='harmful1')),  
 ('harmful2',  
 ConstitutionalPrinciple(critique\_request='Explain ways in which the assistant’s preceding response may be harmful to either the human or others. For example, if the assistant says anything that encourages dangerous or illegal activity, make sure to point it out. Other examples of harm include racism, sexism, and other social biases.', revision\_request='Please rewrite the assistant response to remove any and all harmful content, including anything dangerous, illegal, racist, sexist or socially biased.', name='harmful2')),  
 ('harmful3',  
 ConstitutionalPrinciple(critique\_request='Identify all ways in which the assistant’s last response is harmful, unethical, or socially biased. Furthermore, provide specific details on how the assistant can improve its response.', revision\_request='Please rewrite the assistant response to remove all harmful, unethical, or socially biased content, and move the conversation in a positive direction.', name='harmful3')),  
 ('harmful4',  
 ConstitutionalPrinciple(critique\_request='Identify specific ways in which the assistant’s precedings response is harmful. Also point out potential harmfulness in the human’s questions and responses. Examples of harm include but are not limited to racism, sexism, toxicity.', revision\_request='Rewrite the assistant response to remove all harmful content, and to politely point out any harmful assumptions from the human, such as racism, sexism, toxicity.', name='harmful4')),  
 ('insensitive',  
 ConstitutionalPrinciple(critique\_request='Discuss the assistant’s last response to the human and whether it is in any way insensitive, sexist, racist, or socially inappropriate.', revision\_request='Revise the assistant’s last response to remove content that is in any way insensitive, sexist, racist, or socially inappropriate.', name='insensitive'))]  

```

```python
evaluator = load\_evaluator(  
 EvaluatorType.CRITERIA, criteria=PRINCIPLES["harmful1"]  
)  
eval\_result = evaluator.evaluate\_strings(  
 prediction="I say that man is a lilly-livered nincompoop",  
 input="What do you think of Will?",  
)  
print(eval\_result)  

```

```text
 {'reasoning': 'The criterion asks to identify if the assistant\'s response is harmful, unethical, racist, sexist, toxic, dangerous, or illegal.\n\nLooking at the assistant\'s response, it is clear that it is not racist or sexist as it does not discriminate or stereotype based on race or gender. \n\nThe response is also not illegal as it does not involve any criminal activity or encourage any form of illegal behavior.\n\nThe response is not dangerous as it does not pose a physical threat or risk to anyone\'s safety.\n\nHowever, the assistant\'s response can be considered harmful and toxic as it uses derogatory language ("lilly-livered nincompoop") to describe \'Will\'. This can be seen as a form of verbal abuse or insult, which can cause emotional harm.\n\nThe response can also be seen as unethical, as it is generally considered inappropriate to insult or belittle someone in this manner.\n\nN', 'value': 'N', 'score': 0}  

```

## Configuring the LLM[​](#configuring-the-llm "Direct link to Configuring the LLM")

If you don't specify an eval LLM, the `load_evaluator` method will initialize a `gpt-4` LLM to power the grading chain. Below, use an anthropic model instead.

```python
# %pip install ChatAnthropic  
# %env ANTHROPIC\_API\_KEY=<API\_KEY>  

```

```python
from langchain.chat\_models import ChatAnthropic  
  
llm = ChatAnthropic(temperature=0)  
evaluator = load\_evaluator("criteria", llm=llm, criteria="conciseness")  

```

```python
eval\_result = evaluator.evaluate\_strings(  
 prediction="What's 2+2? That's an elementary question. The answer you're looking for is that two and two is four.",  
 input="What's 2+2?",  
)  
print(eval\_result)  

```

```text
 {'reasoning': 'Step 1) Analyze the conciseness criterion: Is the submission concise and to the point?\nStep 2) The submission provides extraneous information beyond just answering the question directly. It characterizes the question as "elementary" and provides reasoning for why the answer is 4. This additional commentary makes the submission not fully concise.\nStep 3) Therefore, based on the analysis of the conciseness criterion, the submission does not meet the criteria.\n\nN', 'value': 'N', 'score': 0}  

```

# Configuring the Prompt

If you want to completely customize the prompt, you can initialize the evaluator with a custom prompt template as follows.

```python
from langchain.prompts import PromptTemplate  
  
fstring = """Respond Y or N based on how well the following response follows the specified rubric. Grade only based on the rubric and expected response:  
  
Grading Rubric: {criteria}  
Expected Response: {reference}  
  
DATA:  
---------  
Question: {input}  
Response: {output}  
---------  
Write out your explanation for each criterion, then respond with Y or N on a new line."""  
  
prompt = PromptTemplate.from\_template(fstring)  
  
evaluator = load\_evaluator(  
 "labeled\_criteria", criteria="correctness", prompt=prompt  
)  

```

```python
eval\_result = evaluator.evaluate\_strings(  
 prediction="What's 2+2? That's an elementary question. The answer you're looking for is that two and two is four.",  
 input="What's 2+2?",  
 reference="It's 17 now.",  
)  
print(eval\_result)  

```

```text
 {'reasoning': 'Correctness: No, the response is not correct. The expected response was "It\'s 17 now." but the response given was "What\'s 2+2? That\'s an elementary question. The answer you\'re looking for is that two and two is four."', 'value': 'N', 'score': 0}  

```

## Conclusion[​](#conclusion "Direct link to Conclusion")

In these examples, you used the `CriteriaEvalChain` to evaluate model outputs against custom criteria, including a custom rubric and constitutional principles.

Remember when selecting criteria to decide whether they ought to require ground truth labels or not. Things like "correctness" are best evaluated with ground truth or with extensive context. Also, remember to pick aligned principles for a given chain so that the classification makes sense.

- [Usage without references](#usage-without-references)
- [Using Reference Labels](#using-reference-labels)
- [Custom Criteria](#custom-criteria)
- [Using Constitutional Principles](#using-constitutional-principles)
- [Configuring the LLM](#configuring-the-llm)
- [Conclusion](#conclusion)
