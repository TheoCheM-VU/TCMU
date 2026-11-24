# this script requires
# node@18.2.0
# canvas@3.2.3
# jsdom@13.2.0


import subprocess as sp
import os

fonts = [
    "calibri",
    "arial",
    "times new roman",
    "helvetica",
    "garamond",
]

characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁿⁱ₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎ₐₑₒₓₔαβγδεζηθικλμνξοπρστυφχψωΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ.,/?<>{}[]()+-_=^:;%* ᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖʳˢᵗᵘᵛʷˣʸᶻᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾᴿˢᵀᵁⱽᵂˣʸᶻₐₑₕᵢⱼₖₗₘₙₒₚᵣₛₜᵤᵥₓₐₑₕᵢⱼₖₗₘₙₒₚᵣₛₜᵤᵥₓ"

script = """

const jsdom = require("jsdom");
const { JSDOM } = jsdom;

global.document = new JSDOM("<html><head></head></html>").window.document;

function getTextWidth(text, font) {
  const dom = new JSDOM(`<!DOCTYPE html><canvas id="canvas" width="400" height="400"></canvas>`);
  const canvas = dom.window.document.getElementById("canvas");
  const ctx = canvas.getContext("2d"); // Ensure the canvas package is installed
  ctx.font = font;
  var metrics = ctx.measureText(text);
  return metrics.width;
};

let chars = '[CHARACTERS]';
let fonts = [[FONTS]];
for (let j = 0; j < fonts.length; j++) {
  let font = fonts[j];
  for (let i = 0; i < chars.length; i++) {
    console.log(font.replaceAll(" ", "_") + " " + chars[i] + " " + getTextWidth(chars[i], "1pt " + font));
  }
}
""".replace("[CHARACTERS]", characters).replace("[FONTS]", ", ".join(['"' + font + '"' for font in fonts]))

with open("char_width.js", "w+") as js_script:
    js_script.write(script)

with open("_char_widths.txt", "w+") as out:
    for line in sp.check_output(["node", "char_width.js"]).decode().splitlines():
        out.write(line + "\n")

os.remove("char_width.js")
