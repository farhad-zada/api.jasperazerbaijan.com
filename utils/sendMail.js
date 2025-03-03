const nodemailer = require("nodemailer");
const config = require("../config");
const fs = require("fs");

module.exports = async (options, templatePath = null) => {
  // Create the email transporter
  console.log("Creating email transporter...");
  const transporter = nodemailer.createTransport(config.mail_conf);

  try {
    await transporter.verify();
    console.log("Email transporter verified successfully!");
  } catch (verifyError) {
    console.error(
      "Email transporter verification failed:",
      verifyError.message
    );
    throw new Error(`Email server connection error: ${verifyError.message}`);
  }

  // Default template path if none provided
  templatePath =
    templatePath || __dirname + "./mailTemplates/applicationReceived.html";

  // Read and customize the email template
  let emailTemplate = fs.readFileSync(templatePath, "utf8");

  // Replace placeholder for customer name
  emailTemplate = emailTemplate.replace(
    "{{customerName}}",
    options.customerName || "Valued Customer"
  );

  // Define email options
  const mailOptions = {
    from: config.email_username,
    to: options.to,
    subject: options.subject || "Request Received - Jasper Azerbaijan",
    text:
      options.text ||
      "We have received your request and will contact you soon.",
    html: emailTemplate,
  };

  // Send the email
  await transporter.sendMail(mailOptions);
};
