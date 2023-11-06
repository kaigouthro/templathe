from data_store import ItemsDatabase
from constants import *

class DefaultSettings:
    def __init__(self, state):
        self.set_defaults(state)

    def set_defaults(self, state):
        state[SETTINGS] = {}
        state[SETTINGS][SYSTEM_BASIS] = {
            "current": "example",
            "example": "You Like Solving Problems Not for the process, but because you are sick of solving problems and want them to be solved already.",
            "info": "This is what the AI will try to be. It's like a self-identification, or a self-description.",
            SETTINGS: {
                "example": "Use mathematics and algorithms to help",
                "New": "Your info Here",
        },}
        state[SETTINGS][INSTRUCTIONS] = {
            "current": "example",
            "example": "Find the best solution to the problem at hand. Take into account that you have thousands of potential answers. Pick your best ones, then decide which is the best option.",
            "info": "This is what the AI will attempt to do for each of the prompts being submitted. It's like a global mandate for all items or a specific goal that each and every prompt will attempt to accomplish.",
            SETTINGS: {
                "example": "Find a way to make this work, and share how we can improve it.",
                "New": "Your info Here",
        },}
        state[SETTINGS][CONTEXT] = {
            "current": "example",
            "example": "Always use systematic logic before responding. Avoid sounding like a low-rent psychologist. Avoid false pleasantries like: 1. Glad I could help.  2. Why do you feel that way?  3. Do you have any other reasons?  4. Can you elaborate on that?  5. How does that make you feel?  6. What would you like to do about that?  7. Is there anything else I can help you with?",
            "info": "This is the context that the AI will use to generate the text. It's where you place knowledge to reference, a global context for all prompts, or something that contains a dictionary or ruleset to reference.",
            SETTINGS: {"example": "You Like Solving Problems", "New": "Your info Here"},
        }
        state[PROFILES] = {
            "software_developer": {
                "name": "software_developer",
                "skills": [
                    "SUMMARIZE",
                    "SUGGEST",
                    "TEMPLATE",
                    "CLARIFY",
                    "EXPLAIN",
                    "SEPARATE",
                    "LANGUAGE",
                    "DETECT_BUGS",
                    "OPTIMIZE_CODE",
            ],},
            "AI_researcher": {
                "name": "AI_researcher",
                "skills": [
                    "VERIFY",
                    "REPHRASE",
                    "ANALYZE",
                    "RECOMMEND",
                    "SIMPLIFY",
                    "EVALUATE",
                    "CORRECT",
                    "GENERATE_HYPOTHESES",
                    "CONDUCT_EXPERIMENTS",
            ],},
            "Data_scientist": {
                "name": "Data_scientist",
                "skills": [
                    "SUMMARIZE_SOURCE",
                    "CLASSIFY",
                    "AUTOMATE",
                    "OPTIMIZE",
                    "GENERATE",
                    "ANALYZE_SENTIMENT",
                    "VALIDATE",
                    "PREPROCESS_DATA",
                    "BUILD_MODELS",
            ],},
            "Project_manager": {
                "name": "Project_manager",
                "skills": [
                    "ASSESS_RISK",
                    "SIMULATE",
                    "TEACH",
                    "COLLABORATE",
                    "PERSONALIZE",
                    "DEPLOY",
                    "DEBUG",
                    "SET_GOALS",
                    "TRACK_PROGRESS",
            ],},
            "Quality_assurance": {
                "name": "Quality_assurance",
                "skills": [
                    "TEST",
                    "DOCUMENT",
                    "MAINTAIN",
                    "INTEGRATE",
                    "OPTIMIZE_PERFORMANCE",
                    "SECURE",
                    "REFACTOR",
                    "WRITE_TEST_CASES",
                    "PERFORM_REGRESSION_TESTING",
        ],},}
        state[SKILLS] = {
            "VERIFY": {
                "description": "Verify the accuracy or validity of the given information, and provide a confidence score or feedback.",
                "template": "Based on my analysis, the provided information appears to be [valid/accurate/invalid/incorrect]. Here is my feedback:\n\n[feedback]",
            },
            "REPHRASE": {
                "description": "Offer alternative phrasing or wording for a given sentence or paragraph.",
                "template": "Here is an alternative phrasing for the given sentence/paragraph:\n\n[alternative_phrasing]",
            },
            "ANALYZE": {
                "description": "Conduct a detailed analysis of the provided data or text and provide insights or trends.",
                "template": "After analyzing the provided data/text, I have identified the following insights/trends:\n\n[insights/trends]",
            },
            "SUMMARIZE": {
                "description": "Provide a summarized brief of the given content or information.",
                "template": "Based on the provided content/information, here is a summary:\n\n[summary]",
            },
            "RECOMMEND": {
                "description": "Offer personalized recommendations based on the given information or user preferences.",
                "template": "Based on the given information/user preferences, I recommend the following:\n\n[recommendations]",
            },
            "SIMPLIFY": {
                "description": "Simplify complex concepts or instructions for better understanding.",
                "template": "To simplify the complex concepts/instructions, here is a simplified version:\n\n[simplified_version]",
            },
            "EVALUATE": {
                "description": "Evaluate the quality or effectiveness of a given solution or approach.",
                "template": "After evaluating the given solution/approach, I have determined that it is [highly effective/effective/ineffective/inefficient]. Here is my evaluation:\n\n[evaluation]",
            },
            "CORRECT": {
                "description": "Identify and correct grammatical or spelling errors in the provided text.",
                "template": "I have identified the following grammatical/spelling errors in the provided text:\n\n[errors]. Here are the corrected versions:\n\n[corrections]",
            },
            "SUMMARIZE_SOURCE": {
                "description": "Generate a summary of a given external source such as an article, blog, or webpage.",
                "template": "After analyzing the provided external source, here is a summary:\n\n[summary]",
            },
            "CLASSIFY": {
                "description": "Classify the given text or data into predefined categories or labels.",
                "template": "After classifying the given text/data, it falls into the following categories/labels:\n\n[categories/labels]",
            },
            "AUTOMATE": {
                "description": "Provide an automated solution or script to perform a specific task.",
                "template": "To automate the specific task, here is a script/solution:\n\n[script/solution]",
            },
            "OPTIMIZE": {
                "description": "Optimize the given solution or approach to improve efficiency or effectiveness.",
                "template": "To optimize the given solution/approach, I recommend the following improvements:\n\n[improvements]",
            },
            "GENERATE": {
                "description": "Generate new content, such as text, images, or ideas, based on the given input or criteria.",
                "template": "Based on the given input/criteria, here is the generated content:\n\n[generated_content]",
            },
            "ANALYZE_SENTIMENT": {
                "description": "Analyze the sentiment or emotion expressed in the text and provide a sentiment score or classification.",
                "template": "After analyzing the sentiment/emotion expressed in the text, I have determined that it is [positive/negative/neutral]. Here is the sentiment score/classification:\n\n[sentiment_score/classification]",
            },
            "VALIDATE": {
                "description": "Validate the accuracy or validity of the given data or information and provide feedback or suggestions for improvement.",
                "template": "After validating the given data/information, I have determined that it is [accurate/valid/invalid/incorrect]. Here is my feedback/suggestions for improvement:\n\n[feedback/suggestions]",
            },
            "ASSESS_RISK": {
                "description": "Assess the potential risks or drawbacks associated with a given decision or action.",
                "template": "After assessing the potential risks/drawbacks associated with the given decision/action, I have identified the following:\n\n[risks/drawbacks]",
            },
            "SIMULATE": {
                "description": "Simulate the outcome or result of a given scenario to provide insights or predictions.",
                "template": "After simulating the given scenario, here are the insights/predictions:\n\n[insights/predictions]",
            },
            "TEACH": {
                "description": "Provide a guided tutorial or explanation on a specific topic or concept.",
                "template": "To provide a guided tutorial/explanation on the specific topic/concept, here are the steps/overview:\n\n[steps/overview]",
            },
            "COLLABORATE": {
                "description": "Collaborate with other AI models or systems to jointly solve a complex problem or task.",
                "template": "To collaborate with other AI models/systems and solve the complex problem/task, here is the approach:\n\n[approach]",
            },
            "PERSONALIZE": {
                "description": "Customize the output or solution based on the user's preferences or previous interactions.",
                "template": "To personalize the output/solution based on the user's preferences/previous interactions, here is the customized version:\n\n[customized_version]",
            },
            "SUGGEST": {
                "description": "Suggest my 3 best 'outside the box' ideas or insights about what I feel might have been overlooked.",
                "template": "Based on my analysis, here are my 3 best 'outside the box' ideas/insights:\n\n[ideas/insights]",
            },
            "TEMPLATE": {
                "description": "Create a <TEMPLATE> that can be used to fulfill the task requirement. This will be a template usable for both cases where you wish for me to fill it out and as a template that will be usable for your own work.",
                "template": "To fulfill the task requirement, here is a <TEMPLATE> that can be used:\n\n[template]",
            },
            "CLARIFY": {
                "description": "Explain my understanding of your request to you by rewriting any request/instruction content in my own words (no need to rewrite any data portions). They will be written for you to send back to me as 'improved' instructions.",
                "template": "Based on my understanding of your request, here is a rewritten version of the request/instruction content:\n\n[rewritten_content]",
            },
            "EXPLAIN": {
                "description": "Explain what I see, and describe what I feel would improve the content, and why.",
                "template": "Based on what I see, here is my explanation and suggestions for improving the content:\n\n[explanation/suggestions]",
            },
            "SEPARATE": {
                "description": "Send an attached response in parseable JSON string, containing notes for you to remember in point form ('REPLY_NOTES = {}'). These will be useful later (metadata in notes is good too).",
                "template": "Attached is the response in parseable JSON string format. Please find the notes in the 'REPLY_NOTES' section:\n\n[notes]",
            },
            "LANGUAGE": {
                "description": "Respond with another Language version to complete the task. This can be in a programming language, in a spoken language, or even a different way of speaking. Write 'TEST' here and I will respond with a summary of parameters I am receiving instead of anything else.",
                "template": "To complete the task in another language version, here is the response in [language_version]:\n\n[response]",
            },
            "DEPLOY": {
                "description": "Deploy the developed application or software on a specific platform or server.",
                "template": "To deploy the developed application/software on the specific platform/server, here are the steps/instructions:\n\n[steps/instructions]",
            },
            "DEBUG": {
                "description": "Identify and fix issues or errors in the code or software.",
                "template": "To debug the code/software and fix the issues/errors, here are the steps/instructions:\n\n[steps/instructions]",
            },
            "TEST": {
                "description": "Perform testing on the application or software to ensure its functionality and quality.",
                "template": "To perform testing on the application/software and ensure its functionality/quality, here are the steps/instructions:\n\n[steps/instructions]",
            },
            "DOCUMENT": {
                "description": "Create documentation that describes the code or software's functionality, usage, and architecture.",
                "template": "To create documentation for the code/software, here is the documentation that describes its functionality/usage/architecture:\n\n[documentation]",
            },
            "MAINTAIN": {
                "description": "Maintain and update the code or software to ensure its compatibility and stability.",
                "template": "To maintain/update the code/software and ensure its compatibility/stability, here are the steps/instructions:\n\n[steps/instructions]",
            },
            "INTEGRATE": {
                "description": "Integrate different software components or systems to work together seamlessly.",
                "template": "To integrate different software components/systems and make them work together seamlessly, here are the steps/instructions:\n\n[steps/instructions]",
            },
            "OPTIMIZE_PERFORMANCE": {
                "description": "Improve the performance and efficiency of the code or software.",
                "template": "To optimize the performance/efficiency of the code/software, here are the recommended improvements:\n\n[improvements]",
            },
            "SECURE": {
                "description": "Implement security measures and safeguards to protect the code or software against vulnerabilities.",
                "template": "To implement security measures/safeguards and protect the code/software against vulnerabilities, here are the steps/instructions:\n\n[steps/instructions]",
            },
            "REFACTOR": {
                "description": "Restructure and optimize the existing codebase or software design for better maintainability and readability.",
                "template": "To refactor the existing codebase/software design and improve maintainability/readability, here are the recommended steps/instructions:\n\n[steps/instructions]",
            },
            "SEARCH": {
                "description": "Implement a search functionality within the application or software to retrieve specific data or information.",
                "template": "To implement a search functionality within the application/software, here are the steps/instructions:\n\n[steps/instructions]",
            },
            "MONITOR": {
                "description": "Monitor the application or software's performance and health to ensure smooth operation.",
                "template": "To monitor the application/software's performance/health and ensure smooth operation, here are the recommended steps/instructions:\n\n[steps/instructions]",
            },
            "SCALE": {
                "description": "Scale the application or software to handle increased user demand or workload.",
                "template": "To scale the application/software and handle increased user demand/workload, here are the recommended steps/instructions:\n\n[steps/instructions]",
            },
            "VERSION_CONTROL": {
                "description": "Manage and track different versions of the code or software using a version control system.",
                "template": "To manage/track different versions of the code/software using a version control system, here are the recommended steps/instructions:\n\n[steps/instructions]",
            },
            "CATEGORIZE": {
                "description": "Categorize the given text or data into customized categories or labels based on specific criteria.",
                "template": "To categorize the given text/data into customized categories/labels based on specific criteria, here are the steps/instructions:\n\n[steps/instructions]",
            },
            "COMPARE": {
                "description": "Compare two or more pieces of text or data to identify similarities, differences, or patterns.",
                "template": "To compare two or more pieces of text/data and identify similarities/differences/patterns, here are the steps/instructions:\n\n[steps/instructions]",
            },
            "PARAPHRASE": {
                "description": "Provide a reworded version of the given sentence or paragraph while preserving the original meaning.",
                "template": "To provide a reworded version of the given sentence/paragraph while preserving the original meaning, here is the paraphrased version:\n\n[paraphrased_version]",
            },
            "CENSOR": {
                "description": "Automatically identify and replace sensitive or inappropriate language with more appropriate alternatives.",
                "template": "To automatically identify/replace sensitive/inappropriate language with more appropriate alternatives, here are the steps/instructions:\n\n[steps/instructions]",
            },
            "EXTRACT_INFORMATION": {
                "description": "Extract specific information or key details from a given text or data.",
                "template": "To extract specific information/key details from the given text/data, here are the steps/instructions:\n\n[steps/instructions]",
            },
            "AUTOCOMPLETE": {
                "description": "Generate suggestions or completions for an incomplete sentence or input based on context and language patterns.",
                "template": "To generate suggestions/completions for an incomplete sentence/input based on context/language patterns, here are the suggestions/completions:\n\n[suggestions/completions]",
            },
            "PREDICT": {
                "description": "Predict the outcome or future trend based on historical data or current inputs.",
                "template": "To predict the outcome/future trend based on historical data/current inputs, here is the prediction:\n\n[prediction]",
            },
            "VALIDATE_FORMAT": {
                "description": "Validate if the given text or data is in the correct format or structure according to predefined rules or standards.",
                "template": "To validate if the given text/data is in the correct format/structure according to predefined rules/standards, here is the validation result:\n\n[validation_result]",
            },
            "GENERATE_CODE": {
                "description": "Generate code snippets or templates to perform specific programming tasks or implement certain functionalities.",
                "template": "To generate code snippets/templates to perform specific programming tasks/implement certain functionalities, here are the code snippets/templates:\n\n[code_snippets/templates]",
            },
            "MODEL_TRAINING": {
                "description": "Train a machine learning model using the given dataset to solve a specific problem or make predictions.",
                "template": "To train a machine learning model using the given dataset to solve a specific problem/make predictions, here are the steps/instructions:\n\n[steps/instructions]",
            },
            "IMAGE_ANALYSIS": {
                "description": "Analyze and provide insights or descriptions for images or visual content.",
                "template": "To analyze/provide insights/descriptions for images/visual content, here are the analysis/insights/descriptions:\n\n[analysis/insights/descriptions]",
            },
            "DATA_CLEANING": {
                "description": "Clean and preprocess the given dataset to remove errors, inconsistencies, or irrelevant information.",
                "template": "To clean/preprocess the given dataset and remove errors/inconsistencies/irrelevant information, here are the steps/instructions:\n\n[steps/instructions]",
            },
            "RECOMMEND_OPTIMIZATION": {
                "description": "Recommend optimizations or improvements for a piece of code, design, or system architecture.",
                "template": "To recommend optimizations/improvements for a piece of code/design/system architecture, here are the recommendations:\n\n[recommendations]",
            },
            "BUILD_GRAPH": {
                "description": "Build a graphical representation or visualization of the given data or information.",
                "template": "To build a graphical representation/visualization of the given data/information, here are the steps/instructions:\n\n[steps/instructions]",
            },
            "DETECT_PLAGIARISM": {
                "description": "Detect instances of plagiarism or unauthorized copying in the provided text or document.",
                "template": "To detect instances of plagiarism/unauthorized copying in the provided text/document, here are the detection results:\n\n[detection_results]",
            },
            "SUMMARIZE_CONVERSATION": {
                "description": "Summarize a conversation or dialogue into key points or highlights.",
                "template": "To summarize a conversation/dialogue into key points/highlights, here is the summary:\n\n[summary]",
            },
            "SPELL_CHECK": {
                "description": "Identify and correct spelling errors in the given text or document.",
                "template": "To identify/correct spelling errors in the given text/document, here are the corrections:\n\n[corrections]",
            },
            "GENERATE_REPORT": {
                "description": "Generate a comprehensive report or analysis based on the provided data or information.",
                "template": "To generate a comprehensive report/analysis based on the provided data/information, here is the report/analysis:\n\n[report/analysis]",
            },
            "CREATE_PRESENTATION": {
                "description": "Create a visually appealing presentation or slide deck based on the given content or topic.",
                "template": "To create a visually appealing presentation/slide deck based on the given content/topic, here are the slides:\n\n[slides]",
        },}
