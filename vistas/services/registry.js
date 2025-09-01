export function buildRegistry(catalog, catTitles) {
  const byId = new Map();
  const byCat = new Map();

  for (const def of catalog) {
    byId.set(def.id, def);
    if (!byCat.has(def.categoria)) byCat.set(def.categoria, []);
    byCat.get(def.categoria).push(def);
  }
  return { catalog, byId, byCat, catTitles };
}

