"use client";
import { useEffect, useRef, useState } from "react";
import * as Blockly from "blockly/core";
import "blockly/blocks";
import { javascriptGenerator } from "blockly/javascript";

export default function RaindropBlockly() {
  const blocklyDiv = useRef(null);
  const workspaceRef = useRef(null);
  const [generatedCode, setGeneratedCode] = useState("");

  const toolbox = {
    kind: "flyoutToolbox",
    contents: [
      { kind: "block", type: "setup_block" },
      { kind: "block", type: "servo_init" },
      { kind: "block", type: "sensor_init" },
      { kind: "block", type: "sensor_read" },
      { kind: "block", type: "logic_block" },
      { kind: "block", type: "delay_block" },
    ],
  };

  useEffect(() => {
    // === BLOK 1: SETUP ===
    Blockly.Blocks["setup_block"] = {
      init: function () {
        this.appendDummyInput().appendField("Program Utama");
        this.appendStatementInput("DO")
          .setCheck(null)
          .appendField("jalankan blok di bawah ini:");
        this.setColour(210);
      },
    };

    javascriptGenerator.forBlock["setup_block"] = function (block) {
      const statements = javascriptGenerator.statementToCode(block, "DO");
      return `
#include <ESP32Servo.h>
Servo jemuran;
int nilai;
int sensorPin;

void setup() {
  Serial.begin(9600);
${statements}
}

void loop() {
  nilai = analogRead(sensorPin);
  Serial.println(nilai);
${statements}
}
`;
    };

    // === BLOK 2: INISIALISASI SERVO ===
    Blockly.Blocks["servo_init"] = {
      init: function () {
        this.appendDummyInput()
          .appendField("Hubungkan servo ke pin")
          .appendField(
            new Blockly.FieldDropdown([
              ["13", "13"],
              ["12", "12"],
              ["14", "14"],
              ["15", "15"],
            ]),
            "PIN_SERVO"
          );
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(120);
      },
    };

    javascriptGenerator.forBlock["servo_init"] = function (block) {
      const pin = block.getFieldValue("PIN_SERVO");
      return `  jemuran.attach(${pin});\n`;
    };

    // === BLOK 3: INISIALISASI SENSOR ===
    Blockly.Blocks["sensor_init"] = {
      init: function () {
        this.appendDummyInput()
          .appendField("Gunakan sensor hujan di pin")
          .appendField(
            new Blockly.FieldDropdown([
              ["34", "34"],
              ["35", "35"],
              ["32", "32"],
              ["33", "33"],
            ]),
            "PIN_SENSOR"
          );
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(45);
      },
    };

    javascriptGenerator.forBlock["sensor_init"] = function (block) {
      const pin = block.getFieldValue("PIN_SENSOR");
      return `  sensorPin = ${pin};\n`;
    };

    // === BLOK 4: BACA SENSOR ===
    Blockly.Blocks["sensor_read"] = {
      init: function () {
        this.appendDummyInput().appendField("Baca nilai dari sensor hujan");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(270);
      },
    };

    javascriptGenerator.forBlock["sensor_read"] = function () {
      return `  nilai = analogRead(sensorPin);
  Serial.println(nilai);\n`;
    };

    // === BLOK 5: LOGIKA JEMURAN ===
    Blockly.Blocks["logic_block"] = {
      init: function () {
        this.appendDummyInput().appendField("Jika nilai < 2950 maka buka jemuran, jika tidak tutup");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(0);
      },
    };

    javascriptGenerator.forBlock["logic_block"] = function () {
      return `  if (nilai < 2950) {
    jemuran.write(160);
  } else {
    jemuran.write(30);
  }\n`;
    };

    // === BLOK 6: DELAY / JEDA ===
    Blockly.Blocks["delay_block"] = {
      init: function () {
        this.appendDummyInput()
          .appendField("Tunggu selama")
          .appendField(
            new Blockly.FieldDropdown([
              ["500 ms", "500"],
              ["1000 ms", "1000"],
              ["2000 ms", "2000"],
            ]),
            "DELAY_TIME"
          );
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(160);
      },
    };

    javascriptGenerator.forBlock["delay_block"] = function (block) {
      const delayTime = block.getFieldValue("DELAY_TIME");
      return `  delay(${delayTime});\n`;
    };

    // === INIT WORKSPACE ===
    const workspace = Blockly.inject(blocklyDiv.current, { toolbox });
    workspaceRef.current = workspace;
    return () => workspace.dispose();
  }, []);

  const generateCode = () => {
    if (!workspaceRef.current) return;
    const code = javascriptGenerator.workspaceToCode(workspaceRef.current);
    setGeneratedCode(code);
  };

  const downloadCode = () => {
    const blob = new Blob([generatedCode], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "jemuran_otomatis.ino";
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4 text-blue-600">
        💧 IoTown Blockly — Jemuran Otomatis (Versi Edukasi)
      </h1>

      <div className="flex gap-3 mb-4">
        <button
          onClick={generateCode}
          className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded"
        >
          ⚙️ Generate Code
        </button>
        <button
          onClick={downloadCode}
          disabled={!generatedCode}
          className={`${
            generatedCode
              ? "bg-green-500 hover:bg-green-600"
              : "bg-gray-400 cursor-not-allowed"
          } text-white px-4 py-2 rounded`}
        >
          💾 Download .ino
        </button>
      </div>

      <div
        ref={blocklyDiv}
        style={{ height: "500px", width: "100%", backgroundColor: "#f5f5f5" }}
        className="rounded-lg shadow-md mb-4"
      ></div>

      <h2 className="text-lg font-semibold mb-2">🧠 Hasil Kode:</h2>
      <textarea
        className="w-full p-3 border rounded bg-gray-50 font-mono text-sm"
        rows="14"
        value={generatedCode}
        readOnly
      />
    </div>
  );
}
