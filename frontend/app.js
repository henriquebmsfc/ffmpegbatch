async function upload() {
    const files = document.getElementById("fileInput").files;
    for (let f of files) {
        const fd = new FormData();
        fd.append("file", f);
        await fetch("/upload", { method: "POST", body: fd });
    }
    alert("Upload concluído!");
}

async function processar() {
    const r = await fetch("/run-batch");
    const json = await r.json();
    
    const ul = document.getElementById("resultados");
    ul.innerHTML = "";
    json.generated.forEach(file => {
        ul.innerHTML += `<li><a href="/download/${file.split('/').pop()}">${file}</a></li>`;
    });
}
