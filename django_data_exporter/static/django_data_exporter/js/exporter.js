function copyTableToClipboard(tableId) {
    const table = document.getElementById(tableId);
    if (!table) return;

    let tsv = [];
    
    // Get headers
    const headers = Array.from(table.querySelectorAll('th')).map(th => th.innerText.trim());
    tsv.push(headers.join('\t'));
    
    // Get rows
    const rows = table.querySelectorAll('tbody tr');
    rows.forEach(row => {
        const cells = Array.from(row.querySelectorAll('td')).map(td => td.innerText.trim());
        tsv.push(cells.join('\t'));
    });
    
    const fullTsv = tsv.join('\n');
    
    navigator.clipboard.writeText(fullTsv).then(() => {
        showToast();
    }).catch(err => {
        console.error('Error al copiar: ', err);
    });
}

function showToast() {
    let toast = document.getElementById('toast');
    if (!toast) {
        toast = document.createElement('div');
        toast.id = 'toast';
        toast.className = 'toast';
        toast.innerText = '¡Copiado al portapapeles!';
        document.body.appendChild(toast);
    }
    toast.style.display = 'block';
    setTimeout(() => {
        toast.style.display = 'none';
    }, 3000);
}
