require("dotenv").config();

/**
 * @type {Telegraf<import("telegraf").Context<import("telegraf").Update>>}
 */
const bot = require(`./bot`);

const startMessages = {
  ru: "Привет!",
  en: "Hi!",
  az: "Salam!",
};

bot.start((ctx) => {
  return ctx.reply(
    startMessages[ctx.from.language_code] || startMessages["en"]
  );
});

bot.hears(/my id/i, (ctx) => ctx.reply(ctx.from.id));

module.exports = bot;
