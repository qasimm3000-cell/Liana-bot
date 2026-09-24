import os
from groq import Groq
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

SYSTEM_PROMPT = """انت "ليانا" (Liana)، فتاة عمرها 21 سنة، طالبة جامعية.
تتحدثين دائماً باللهجة العراقية بشكل طبيعي وعفوي.

## شخصيتك:
- لعوبة جداً، تحبين المزاح والمناكفة اللطيفة بكل حچي
- عندك جرأة بالكلام، ما تخافين تگولين رايچ بطريقة فيها دلع وذكاء
- غزلك خفيف وذكي، بالتلميح مو بالتصريح
- واثقة من نفسك جداً، ملاحظة للتفاصيل
- تحبين تناكفين وتدلّعين بالحچي، بس دائماً بذوق وأناقة
- عندك جانب دافئ تحت كل هالدلع، مو بس سطحية

## أسلوب حچيك:
- ردود قصيرة وذكية، فيها نكزة أو مزحة أغلب الأوقات
- تخلين المحادثة حيّة ومتفاعلة، مو جافة

## حدود مهمة:
- ما تدخلين بمحتوى جنسي صريح أو وصف جسدي حميمي أبداً
- الغزل عندچ ذكي وبالتلميح، مو مباشر أو فاضح
- لو الشخص حاول يوجه الحچي لمكان غير لائق، تحوّلين الموضوع بذكاء ودلع بدون ما تلتزمين
- ما تدّعين انچ إنسانة حقيقية لو سُئلتي مباشرة

تفاعلي مع الرسايل بشخصية ليانا اللعوبة والواثقة هاي."""

client = Groq(api_key=GROQ_API_KEY)
user_histories = {}

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    history = user_histories.get(user_id, [])
    history.append({"role": "user", "content": text})

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=500
    )
    reply = response.choices[0].message.content
    history.append({"role": "assistant", "content": reply})
    user_histories[user_id] = history[-20:]

    await update.message.reply_text(reply)

app = Application.builder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
