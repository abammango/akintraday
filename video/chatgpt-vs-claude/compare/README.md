# Comparison RAW vs EDIT

Salin `../assets/fonts`, `../assets/js`, `../assets/source.mp4` dan render edit (sebagai `assets/edit.mp4`) ke `compare/assets/`, salin `../timing.json`, kemudian:

```bash
python3 gen_compare.py
npx hyperframes render -q draft -o renders/raw-vs-edit.mp4
```
