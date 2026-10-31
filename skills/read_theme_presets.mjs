// Read literal theme data with the TypeScript parser; never evaluate downloaded source.
import ts from "../sidecar/web/node_modules/typescript/lib/typescript.js";
import fs from "node:fs";

const source = ts.createSourceFile("presets.ts", fs.readFileSync(process.argv[2], "utf8"), ts.ScriptTarget.Latest, true);
function literal(node) {
  if (ts.isStringLiteral(node) || ts.isNumericLiteral(node)) return node.text;
  if (ts.isObjectLiteralExpression(node)) return Object.fromEntries(node.properties.map(p => {
    if (!ts.isPropertyAssignment(p) || !p.name || !p.initializer) throw new Error("Non-literal theme property");
    return [p.name.text, literal(p.initializer)];
  }));
  throw new Error("Non-literal theme value: " + ts.SyntaxKind[node.kind]);
}
let presets;
for (const statement of source.statements) {
  if (!ts.isVariableStatement(statement)) continue;
  for (const decl of statement.declarationList.declarations) {
    if (decl.name.getText(source) === "defaultPresets") presets = literal(decl.initializer);
  }
}
if (!presets || !Object.keys(presets).length) throw new Error("Missing defaultPresets");
process.stdout.write(JSON.stringify(presets));
