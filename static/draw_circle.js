Blockly.Blocks['draw_circle'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Draw Circle");
    this.appendValueInput("radius")
        .setCheck(null)
        .appendField("Raiud");
    this.appendValueInput("xx")
        .setCheck(null)
        .appendField("X");
    this.appendValueInput("yy")
        .setCheck(null)
        .appendField("Y");
    this.setColour(150);
 this.setTooltip("");
 this.setHelpUrl("");
  }
};