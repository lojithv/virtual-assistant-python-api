import express from "express";
import { questionsAndAnswers } from "./dataset";
const mongoose = require("mongoose");
const app = express();
const port = 4000;

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});

main()
  .then(() => seedData())
  .catch((err) => console.log(err));

async function main() {
  await mongoose.connect("mongodb://127.0.0.1:27017/chatbotdb");
}

const datasetSchema = new mongoose.Schema({
  q: String,
  a: String,
});

const Dataset = mongoose.model("Dataset", datasetSchema);

const seedData = async () => {
  for (const data of questionsAndAnswers) {
    const newData = new Dataset({ q: data.q, a: data.a });
    await newData.save();
    console.log("saved")
  }
};
