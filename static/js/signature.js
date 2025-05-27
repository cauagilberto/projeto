const canvas = document.getElementById('signatureCanvas');
const ctx = canvas.getContext('2d');
let drawing = false;

canvas.addEventListener('mousedown', () => drawing = true);
canvas.addEventListener('mouseup', () => drawing = false);
canvas.addEventListener('mouseout', () => drawing = false);
canvas.addEventListener('mousemove', draw);

function draw(event) {
    if (!drawing) return;
    ctx.lineWidth = 2;
    ctx.lineCap = 'round';
    ctx.strokeStyle = 'black';

    const rect = canvas.getBoundingClientRect();
    ctx.lineTo(event.clientX - rect.left, event.clientY - rect.top);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(event.clientX - rect.left, event.clientY - rect.top);
}

function limparAssinatura() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}

document.getElementById('registroForm').addEventListener('submit', function(e) {
    e.preventDefault();

    // Capturar assinatura como imagem
    const dataURL = canvas.toDataURL('image/png');

    const formData = new FormData();
    formData.append('nome', this.nome.value);
    formData.append('numero', this.numero.value);
    formData.append('peso_bruto', this.peso_bruto.value);
    formData.append('peso_liquido', this.peso_liquido.value);
    formData.append('destino', this.destino.value);
    formData.append('assinatura', dataURL);

    fetch('/', {
        method: 'POST',
        body: new URLSearchParams(formData)
    }).then(res => res.json())
     .then(data => {
         alert("Registro salvo com sucesso!");
         location.reload();
     });
});