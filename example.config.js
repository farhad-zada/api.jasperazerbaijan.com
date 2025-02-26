require("dotenv").config();

function validateConfig(config) {
  if (!config.port) {
    throw new Error("\x1b[31mPort is not defined in config.js\x1b[0m");
  }
  if (!config.environment) {
    throw new Error("\x1b[31mEnvironment is not defined in config.js\x1b[0m");
  }
  if (config.email_service === undefined) {
    throw new Error("\x1b[31mEmail service is not defined in config.js\x1b[0m");
  }

  if (!config.email_username) {
    throw new Error(
      "\x1b[31mEmail username is not defined in config.js\x1b[0m"
    );
  }
  if (!config.email_password) {
    throw new Error(
      "\x1b[31mEmail password is not defined in config.js\x1b[0m"
    );
  }
  console.log("\x1b[32m[nous] config validated successfully!\x1b[0m");
}

module.exports = {
  port: process.env.PORT || 8181,
  environment: "development",
  validateConfig,
  email_service: "",
  email_username: "",
  email_password: "",
  allowedOrigins: "",
  tg: {
    chatId: process.env.TG_CHAT_ID, 
    chats: process.env.TG_CHATS.split(","),
  }
};
