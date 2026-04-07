import gradio as gr
import random
import pandas as pd

def generate_random_list(size=10):  #This function creates a random list of integers.
    LOWER_BOUND = 1
    UPPER_BOUND = 100

    return random.sample(range(LOWER_BOUND, UPPER_BOUND), size) #random.sample so all numbers are unique, no repitition.


def bubble_sort(input_list):  #It returns would return final list arranged with the total number of swaps that were made

    a = input_list[:]
    steps = []         # this will store all steps for display
    step_count = 1
    swap_count = 0
    n = len(a)

    # Outer loop = number of passes
    for i in range(n):
        swapped_in_pass = False  # this to find out if list is already sorted

        # Inner for loop is for comparisons between the nubers.
        for j in range(0, n - i - 1):
            left = a[j]
            right = a[j + 1]
            # Step: comparing two elements
            description = (
                f"Pass {i + 1}: Comparing positions {j} and {j + 1} "
                f"({left} vs {right}).")


            steps.append([step_count, i + 1, a[:], j, j + 1, description])
            step_count += 1

            # If left value is bigger, swap
            if left > right:
                a[j], a[j + 1] = a[j + 1], a[j]
                swap_count += 1
                swapped_in_pass = True

                description = (
                    f"{left} is greater than {right}, so we swap them. "
                    f"This moves the larger value to the right."
                )

                steps.append([step_count, i + 1, a[:], j, j + 1, description])
                step_count += 1

            else:
                description = (
                    f"No swap needed because {left} is already less than or equal to {right}."
                )

                steps.append([step_count, i + 1, a[:], j, j + 1, description])
                step_count += 1

        # If no swaps happened, list is already sorted
        if not swapped_in_pass:
            explanation = (
                f"No swaps occurred in Pass {i + 1}, so the list is already sorted."
            )

            steps.append([step_count, i + 1, a[:], "-", "-", explanation])
            step_count += 1
            break

    explanation = f"Sorting complete. Final list: {a}. Total swaps: {swap_count}."

    steps.append([step_count, "-", a[:], "-", "-", explanation])

    return a, steps, swap_count


def create_new_list():

    # when user user clicks 'Generate', it Creates a list and displays it.
    new_list = generate_random_list()
    return new_list, f"**Current List:** {new_list}"


def run_sort(current_list):

    if not current_list:
        return "Please generate a list first!", pd.DataFrame()  #this is for if the user didnt click generate, to stop the app from showing error

    if current_list == sorted(current_list):
        message = "### This list is already sorted."

        df = pd.DataFrame(
            [[1, "-", current_list, "-", "-", "No changes needed."]],
            columns=["Step", "Pass", "Current List", "Index 1", "Index 2", "Action"]
        )

        return message, df

    sorted_list, steps_log, swap_count = bubble_sort(current_list)

    result_msg = (
        f"### ✅ Sorted List: {sorted_list}\n\n"
        f"Bubble Sort works by repeatedly comparing adjacent values and pushing larger values to the end.\n\n"
        f"Total swaps made: {swap_count}"
    )

    headers = ["Step", "Pass", "Current List", "Index 1", "Index 2", "Action"]
    df = pd.DataFrame(steps_log, columns=headers)

    return result_msg, df




with gr.Blocks(theme=gr.themes.Soft()) as demo:


    gr.Markdown("""
    # Bubble Sort in Action, STAY TUNED

    Thanks for downloading my app, I'm going to show you how Bubble Sort works step by step.

    Bubble Sort compares adjacent like side to side numbers and swaps them if they are in the wrong order.
    Over time, larger numbers move "bubble" to the end of the list.

    Now it's your turn, try generating a list and running the algorithm to see each step clearly.
    """)


    list_state = gr.State([])


    with gr.Row():
        with gr.Column(scale=1):
            generate_btn = gr.Button("1. Generate Random List", variant="primary")
        with gr.Column(scale=3):
            list_display = gr.Markdown("**Current List:** (Click generate to start)")

    gr.HTML("<hr>")  # divider line


    with gr.Row():
        with gr.Column(scale=1):
            sort_btn = gr.Button("2. Run Bubble Sort", variant="secondary")

        with gr.Column(scale=3):
            result_output = gr.Markdown("### Ready to sort...")

    gr.Markdown("### Step-by-Step Execution Log")

    steps_output = gr.Dataframe(
        headers=["Step", "Pass", "Current List", "Index 1", "Index 2", "Action"],
        interactive=False,
        wrap=True
    )


    generate_btn.click(      # When the generate button is clicked
        fn=create_new_list,
        inputs=None,
        outputs=[list_state, list_display]
    )


    sort_btn.click(  #sort button
        fn=run_sort,
        inputs=[list_state],
        outputs=[result_output, steps_output]
    )




if __name__ == "__main__":
    demo.launch()