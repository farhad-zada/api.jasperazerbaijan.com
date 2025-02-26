const router = require("express").Router();

const { sendAplication } = require("../controllers/aplicationController");

router.post("/apply", sendAplication);

module.exports = router;
