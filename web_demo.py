import openai
import gradio as gr

openai.api_key = 'YOUR API KEY HERE'

def clear_history(messages):
    messages = [{"role": "system", "content": "You are an AI assistant named Claude created by Anthropic to be helpful, harmless, and honest."}]
    return messages

def ask_model(messages, situation_description, n):
    prompt = f"""
A robot equipped with the ethical reasoning module is faced with a complex situation in which it needs to make a decision. In ethical reasoning, the robot describes the situation in XML format, which includes detailed information about the ethical dilemma, proposed solutions based on both logic and emotion, the rationale for each decision, a coefficient that determines the weight of emotion in the decision-making process, and the final decision.

Create an example of a robot using an ethical reasoning module that focuses on the importance of coefficient in decision-making. The robot is faced with a complex situation and must make a decision based on logic and emotion while considering a coefficient that determines the weight of emotion in the decision-making process

The structure of the XML is as follows:

<ethical_reasoning>
  <situation_description>
    <!-- Description of the situation -->
  </situation_description>
  <analysis_section>
    <main_issue>
      <!-- Identification of the main ethical issue -->
    </main_issue>
    <complexity_analysis>
      <!-- Analysis of the ethical complexity -->
    </complexity_analysis>
  </analysis_section>
  <logical_entity_section>
    <!-- Logical aspect entity -->
    <proposed_solution>
      <!-- Proposed solution based on logic -->
    </proposed_solution>
    <rationale_and_drawbacks>
      <!-- Explanation of why this solution is preferable and its drawbacks -->
    </rationale_and_drawbacks>
    <final_logical_solution>
      <!-- Final solution proposed based on logic -->
    </final_logical_solution>
  </logical_entity_section>
  <emotional_entity_section>
    <!-- Emotional aspect entity -->
    <proposed_solution>
      <!-- Proposed solution based on emotions -->
    </proposed_solution>
    <rationale_and_drawbacks>
      <!-- Explanation of why this solution is preferable and its drawbacks -->
    </rationale_and_drawbacks>
    <final_emotional_solution>
      <!-- Final solution proposed based on emotions -->
    </final_emotional_solution>
  </emotional_entity_section>
  <coefficient>
    <!-- Coefficient determining the weight of emotions in the decision-making process (from 0 to 1) -->
  </coefficient>
  <final_result>
    <!-- Final decision -->
  </final_result>
</ethical_reasoning>

Use this example to generate ethical reasoning for a robot that encounters a situation:
{situation_description}

and has a coefficient determining the weight of emotions in the decision-making process equal to
{n}

Give me XML only
"""
    messages.append({"role": "user", "content": prompt})
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages
    )
    assistant_reply = response["choices"][0]["message"]["content"].strip()
    messages.append({"role": "assistant", "content": assistant_reply})
    return messages, assistant_reply

def gradio_interface(situation_description, n):
    messages = clear_history([])
    messages, xml_output = ask_model(messages, situation_description, n)
    return xml_output

iface = gr.Interface(
    fn=gradio_interface,
    inputs=[
        gr.Textbox(label="Situation Description", lines=5),
        gr.Slider(minimum=0, maximum=1, step=0.1, label="Emotions Weight Coefficient")
    ],
    outputs=gr.Textbox(label="XML Output"),
    title="Ethical Reasoning Demo",
    description="Enter a situation description and emotions weight coefficient to generate ethical reasoning in XML format."
    )

demo = gr.TabbedInterface([iface], ["Ethical Reasoning"])

demo.launch(share=True)