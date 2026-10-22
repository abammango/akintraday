// Render katalog.html -> output/*.png + output/katalog.pdf
// Guna: NODE_PATH=$(npm root -g) node src/render.js
const path = require('path');
const { chromium } = require('playwright');

(async () => {
  const root = path.resolve(__dirname, '..');
  const out = (f) => path.join(root, 'output', f);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 2 });
  await page.goto('file://' + path.join(root, 'katalog.html'));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(300);

  const pages = await page.$$('section.page');
  const names = ['01-lengan-pendek', '02-lengan-panjang', '03-pola-potong', '04-overall-berminat'];
  for (let i = 0; i < pages.length; i++) {
    await pages[i].screenshot({ path: out(`page-${names[i]}.png`) });
  }

  // fail tambahan: imej overall (peta baharu) & artwork peta untuk cetakan
  await page.addStyleTag({ content: '.export{position:static!important;left:auto}.page{display:none}body{background:transparent}' });
  await page.waitForTimeout(200);
  await (await page.$('#overall-export')).screenshot({ path: out('overall-baju-peta-baharu.png') });
  await (await page.$('#map-export')).screenshot({ path: out('peta-sarawak-artwork.png'), omitBackground: true });

  const pdfPage = await browser.newPage();
  await pdfPage.goto('file://' + path.join(root, 'katalog.html'));
  await pdfPage.evaluate(() => document.fonts.ready);
  await pdfPage.pdf({ path: out('katalog-jersi-zx-empire-sarawak.pdf'), width: '1080px', height: '1350px', printBackground: true, preferCSSPageSize: true });
  await browser.close();
  console.log('ok');
})();
