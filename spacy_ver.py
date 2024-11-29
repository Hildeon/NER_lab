import spacy
import gradio as gr

nlp = spacy.load("uk_core_news_sm")

def highlight_proper_nouns(text):
    doc = nlp(text)
    highlighted_text = text
    for ent in reversed(doc.ents):
        if ent.label_ in {"LOC", "ORG", "PER", "MISC", "GPE"}:
            highlighted_text = (
                highlighted_text[:ent.start_char]
                + f"<span style='color:blue; font-weight:bold;'>{ent.text}</span>"
                + highlighted_text[ent.end_char:]
            )
    return highlighted_text

def process_text(text):
    doc = nlp(text)
    proper_nouns = [
        f"{ent.text} ({ent.label_})"
        for ent in doc.ents
        if ent.label_ in {"LOC", "ORG", "PER", "MISC", "GPE"}
    ]
    proper_nouns_result = "\n".join(proper_nouns) if proper_nouns else "Власні назви не знайдено."

    highlighted_text = highlight_proper_nouns(text)
    return (
        gr.update(value=f"Текст із власними назвами виділеними <span style='color:blue; font-weight:bold;'> "
                        f"синім </span> кольором:", visible=True),
        gr.update(value=highlighted_text, visible=True),
        gr.update(value=proper_nouns_result, visible=True)
    )

description = """
### Опис значень типів власних назв:

- **LOC (Location)**: Локація або географічне місце, наприклад, міста, села, вулиці.
- **ORG (Organization)**: Організація, компанія або інші об'єднання, наприклад, компанії, школи, організації.
- **PER (Person)**: Персоналія, людина, або назва особи.
- **GPE (Geopolitical Entity)**: Геополітична одиниця, що включає країни, міста, регіони.
- **MISC (Miscellaneous)**: Інші категорії, що не підпадають під жодну з попередніх.
"""

instruction = """
1. Відкрийте програму через веб-браузер
2. На головній сторінці:
    2.1 	Введіть текст у текстове поле;
    2.2 	Натисніть кнопку "Проаналізувати".
3. Ознайомтеся з результатами:
    3.1 	Текст із виділеними назвами з’явиться у синьому кольорі;
    3.2 	Список знайдених назв відобразиться окремо.
4. Використовуйте вкладку "Інформація про типи назв" для довідки щодо категорій.
- УВАГА!!! Будь-які неточності у визначенні власних назв пов'язані з обмеженою кілкістю даних, що обробляє модель spaCy

"""
with gr.Blocks() as demo:
    with gr.Tab("Головна"):
        with gr.Column():
            gr.Markdown("<h2>Визначення власних назв у тексті 🔍</h2>")
            gr.Markdown(
                "Введіть текст українською мовою, щоб отримати список власних назв і текст із виділеними назвами."
            )
        with gr.Row():
            with gr.Column(scale=1):
                input_text = gr.Textbox(
                    label="",
                    lines=10,
                    placeholder="Введіть текст тут..."
                )
                submit_button = gr.Button("Проаналізувати")
                gr.Markdown("""
                            <p style="font-size: 0.85em; color: gray;">
                                Підтримуються власні назви місць, організацій, людей, тощо.
                            </p>
                            """)

            with gr.Column(scale=1):
                title_html = gr.Markdown(visible=False)
                result_html = gr.HTML(visible=False)
                result_textbox = gr.Textbox(label="Знайдені власні назви: ", visible=False)

        examples = gr.Examples(
            examples=[
                ("Під час відвідування Риму, ми вирішили піднятися на вершину Колізею, щоб помилуватися панорамою "
                 "Форуму Роману, а потім відвідати Ватиканські музеї та побачити Сикстинську капелу."),
                ("На фестивалі 'Atlas Weekend' гурт 'Океан Ельзи' презентував нову пісню, "
                 "а співачка Джамала виконала свій хіт, який переміг на 'Євробаченні'."),
            ],
            inputs=input_text,
            label="Приклади тексту"
        )

    with gr.Tab("Інформація про типи назв"):
        gr.Markdown(description)

    with gr.Tab("Інструкція по використанню"):
        gr.Markdown(instruction)

    gr.HTML("""
    <hr>
    <p style="text-align: center; font-size: 0.85em; color: gray;">
    Розроблено за фінансової підтримки компанії-мецената 'фан-клуб пені жломодєла' 💙💛
    </p>
    """)

    submit_button.click(
        process_text,
        inputs=input_text,
        outputs=[title_html, result_html, result_textbox],
    )

demo.launch()
