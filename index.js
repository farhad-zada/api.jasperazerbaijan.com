const express = require("express");
const helmet = require("helmet");
const cookieParser = require("cookie-parser");
const cors = require("cors");
const app = express();
const config = require("./config");
const logger = require("./utils/logger");
const ExpressMongoSanitize = require("express-mongo-sanitize");
const rateLimit = require("express-rate-limit");

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Limit each IP to 100 requests per windowMs
  message: {
    status: false,
    message: "Too many requests, please try again later.",
  },
  headers: true, // Include rate limit headers in the response
  standardHeaders: true, // Send `RateLimit-*` headers
  legacyHeaders: false, // Disable the `X-RateLimit-*` headers
});

config.validateConfig(config);

require("dotenv").config();

app.use(cookieParser());
app.use(limiter);
app.use(
  cors({
    origin: config.allowedOrigins,
    methods: "POST",
    credentials: true,
  })
);
app.use(
  helmet({
    contentSecurityPolicy: true, // Disable CSP if it's conflicting
  })
);

app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(ExpressMongoSanitize());
app.use((req, res, next) => {
  logger.info(`${req.ip} ${req.method} ${req.url}`);
  next();
});

app.use("/api/v1", require("./routes/api"));

app.use("*", (req, res) =>
  res.status(404).json({ status: false, message: "You hit a wrong route! 🤫" })
);

const server = app.listen(config.port, () => {
  console.log(`Server is running on port ${config.port}`);
});
