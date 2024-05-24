const expandBtn = document.querySelector('#expandBtn');
  const Parent = document.querySelector('#spreadsheetContainer');
  const hot = new Handsontable(document.querySelector('#spreadsheet'), {
    data: new Array(100).fill().map((_, row) => new Array(50).fill().map((_, column) => `${row}, ${column}`)),
    rowHeaders: true,
    colHeaders: true,
    width: '100%',
    height: '410px',
    rowHeights: 23,
    colWidths: 100,
    autoWrapRow: true,
    autoWrapCol: true,
    licenseKey: 'non-commercial-and-evaluation'
  });

  expandBtn.addEventListener('click', () => {
    if (Parent.classList.contains('expanded')) {
      Parent.classList.remove('expanded');
      expandBtn.innerHTML = '<i class="bi bi-arrows-angle-expand"></i>';
    } else {
      Parent.classList.add('expanded');
      expandBtn.innerHTML = '<i class="bi bi-arrows-angle-contract"></i>';
    }
    hot.render();
  });