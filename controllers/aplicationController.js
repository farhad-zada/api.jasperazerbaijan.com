const config = require("../config");
const bot = require("../telegram/bot");
const sendMail = require("../utils/sendMail");

/**
 *
 * @param {import('express').Request} req
 * @param {import('express').Response} res
 */
async function sendAplication(req, res) {
  try {
    const { name, email, phone, tgHandle, message, tags } = req.body;

    if (!name || (!email && validator.isEmail(email))) {
      return res
        .status(400)
        .json({ status: false, message: "Please fill all fields" });
    }
    const msgString = `New application received\nName: ${name}\nEmail: ${email}\nPhone: ${phone}\nTelegram Handle: ${tgHandle}\nMessage: ${message}\n\nTags: ${tags.join(
      ", "
    )}`;

    for (let chatId of config.tg.chats) {
      await bot.telegram.sendMessage(chatId, msgString);
    }

    // Send email
    await sendMail(
      {
        to: email,
        subject: "Application Received - Jasper Azerbaijan",
        customerName: name,
      },
      __dirname + "/../utils/mailTemplates/applicationReceived.html"
    );

    res
      .status(200)
      .json({ status: true, message: "Application sent successfully" });
  } catch (error) {
    console.error(error);
    res.status(500).json({ status: false, message: "Internal Server Error" });
  }
}

module.exports = {
  sendAplication,
};
