// Carrega templates
var collapseHeadTemplate = Handlebars.compile($("#collapse-head").html());
var robsonTableTemplate = Handlebars.compile($("#robson-table").html());

var robsonData = {}

// Valores referência
var robsonRef = {
  G1R1: 0.098, G1R2: 0.293, G1R3: 0.029,
  G2R1: 0.399, G2R2: 0.088, G2R3: 0.035,
  G3R1: 0.030, G3R2: 0.401, G3R3: 0.012,
  G4R1: 0.237, G4R2: 0.064, G4R3: 0.015,
  G5R1: 0.744, G5R2: 0.072, G5R3: 0.053,
  G6R1: 0.785, G6R2: 0.012, G6R3: 0.009,
  G7R1: 0.738, G7R2: 0.015, G7R3: 0.011,
  G8R1: 0.577, G8R2: 0.009, G8R3: 0.005,
  G9R1: 0.886, G9R2: 0.004, G9R3: 0.003,
  G10R1: 0.251, G10R2: 0.042, G10R3: 0.010,
  GTR1: 0.185, GTR2: 1.000, GTR3: 0.185
}


$("#csv").change(function () {

    // Limpa HTML
    $("#accordion").empty();

    Papa.parse(this.files[0], {
      header: true,
      step: function(results) {
        robson = results.data[0];
        id = robson["CODESTAB"];

        // Remove linhas vazias
        if (id == "")
          return;

        // Garante que CSV foi lido como valores inteiros, ao invés de Strings
        Object.keys(robson).map(function(key, index) {
           robson[key] = parseInt(robson[key]);
        });

        // Total de cesáreas
        totalCS = robson["G1C"] + robson["G2C"] + robson["G3C"] + robson["G4C"] +
          robson["G5C"] + robson["G6C"] + robson["G7C"] + robson["G8C"] + robson["G9C"] +
          robson["G10C"];

        // Total de partos vaginais
        totalV = robson["G1V"] + robson["G2V"] + robson["G3V"] + robson["G4V"] +
          robson["G5V"] + robson["G6V"] + robson["G7V"] + robson["G8V"] + robson["G9V"] +
          robson["G10V"];

        // Total de partos
        totalBirth = totalCS + totalV;

        // Calcula valores a serem exibidos
        robsonData[id] = {
          G1C: robson["G1C"],
          G1T: robson["G1C"] + robson["G1V"],
          G1M1: robson["G1C"] / (robson["G1C"] + robson["G1V"]),
          G1R1: robsonRef["G1R1"],
          G1M2: robson["G1C"] / totalCS,
          G1R2: robsonRef["G1R2"],
          G1M3: robson["G1C"] / totalBirth,
          G1R3: robsonRef["G1R3"],
          G2C: robson["G2C"],
          G2T: robson["G2C"] + robson["G2V"],
          G2M1: robson["G2C"] / (robson["G2C"] + robson["G2V"]),
          G2R1: robsonRef["G2R1"],
          G2M2: robson["G2C"] / totalCS,
          G2R2: robsonRef["G2R2"],
          G2M3: robson["G2C"] / totalBirth,
          G2R3: robsonRef["G2R3"],
          G3C: robson["G3C"],
          G3T: robson["G3C"] + robson["G3V"],
          G3M1: robson["G3C"] / (robson["G3C"] + robson["G3V"]),
          G3R1: robsonRef["G3R1"],
          G3M2: robson["G3C"] / totalCS,
          G3R2: robsonRef["G3R2"],
          G3M3: robson["G3C"] / totalBirth,
          G3R3: robsonRef["G3R3"],
          G4C: robson["G4C"],
          G4T: robson["G4C"] + robson["G4V"],
          G4M1: robson["G4C"] / (robson["G4C"] + robson["G4V"]),
          G4R1: robsonRef["G4R1"],
          G4M2: robson["G4C"] / totalCS,
          G4R2: robsonRef["G4R2"],
          G4M3: robson["G4C"] / totalBirth,
          G4R3: robsonRef["G4R3"],
          G5C: robson["G5C"],
          G5T: robson["G5C"] + robson["G5V"],
          G5M1: robson["G5C"] / (robson["G5C"] + robson["G5V"]),
          G5R1: robsonRef["G5R1"],
          G5M2: robson["G5C"] / totalCS,
          G5R2: robsonRef["G5R2"],
          G5M3: robson["G5C"] / totalBirth,
          G5R3: robsonRef["G5R3"],
          G6C: robson["G6C"],
          G6T: robson["G6C"] + robson["G6V"],
          G6M1: robson["G6C"] / (robson["G6C"] + robson["G6V"]),
          G6R1: robsonRef["G6R1"],
          G6M2: robson["G6C"] / totalCS,
          G6R2: robsonRef["G6R2"],
          G6M3: robson["G6C"] / totalBirth,
          G6R3: robsonRef["G6R3"],
          G7C: robson["G7C"],
          G7T: robson["G7C"] + robson["G7V"],
          G7M1: robson["G7C"] / (robson["G7C"] + robson["G7V"]),
          G7R1: robsonRef["G7R1"],
          G7M2: robson["G7C"] / totalCS,
          G7R2: robsonRef["G7R2"],
          G7M3: robson["G7C"] / totalBirth,
          G7R3: robsonRef["G7R3"],
          G8C: robson["G8C"],
          G8T: robson["G8C"] + robson["G8V"],
          G8M1: robson["G8C"] / (robson["G8C"] + robson["G8V"]),
          G8R1: robsonRef["G8R1"],
          G8M2: robson["G8C"] / totalCS,
          G8R2: robsonRef["G8R2"],
          G8M3: robson["G8C"] / totalBirth,
          G8R3: robsonRef["G8R3"],
          G9C: robson["G9C"],
          G9T: robson["G9C"] + robson["G9V"],
          G9M1: robson["G9C"] / (robson["G9C"] + robson["G9V"]),
          G9R1: robsonRef["G9R1"],
          G9M2: robson["G9C"] / totalCS,
          G9R2: robsonRef["G9R2"],
          G9M3: robson["G9C"] / totalBirth,
          G9R3: robsonRef["G9R3"],
          G10C: robson["G10C"],
          G10T: robson["G10C"] + robson["G10V"],
          G10M1: robson["G10C"] / (robson["G10C"] + robson["G10V"]),
          G10R1: robsonRef["G10R1"],
          G10M2: robson["G10C"] / totalCS,
          G10R2: robsonRef["G10R2"],
          G10M3: robson["G10C"] / totalBirth,
          G10R3: robsonRef["G10R3"],
          GTC: totalCS,
          GTT: totalBirth,
          GTM1: totalCS / totalBirth,
          GTR1: robsonRef["GTR1"],
          GTM2: 1,
          GTR2: 1,
          GTM3: totalCS / totalBirth,
          GTR3: robsonRef["GTR3"]
        }

        // Formata números no padrão desejado
        Object.keys(robsonData[id]).map(function(key, index) {
          if (!(["C", "T"].includes(key.slice(-1)))) {
           robsonData[id][key] = ((robsonData[id][key] || 0) * 100).toFixed(2);
          }
        });

        // Gera HTML
        $("#accordion").append(collapseHeadTemplate({HospitalID: id, Score: robson["SCORE"]}));
        $("#p" + id).append(robsonTableTemplate(robsonData[id]));
      }
    });
});
