from Interpret import Interpret

intp =Interpret()
intp.add_header("اطلاعات  کلی", level = 1)
intp.add_header("اطلاعات  کلی", level = 2)
intp.add_text("سلام خوبی؟")
intp.add_text("دیگه چه خبر؟")
intp.add_paragraph("چند سالته؟")
intp.add_paragraph("مجردی؟")
intp.add_paragraph("کارت چیه؟")
intp.add_italic_and_bold_text("دیگه چه خبراااا؟")
intp.line_break()

intp.add_paragraphs(["بقیه سلام میرسونن" , "کی میرسی"])


intp.add_header("اطلاعات  جزئی", level = 1)
intp.add_header("پرسشنامه", level = 2)


print(intp.get_text())

with open(r"C:\Users\mostafa\Desktop\Majazeh\risloo-samples/out.md",'w' , encoding='utf-8') as file:
    file.write(intp.get_text())