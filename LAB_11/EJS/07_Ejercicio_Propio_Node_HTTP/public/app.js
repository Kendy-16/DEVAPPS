async function cargar(){try{const r=await fetch('/api/estacion');const x=await r.json();document.getElementById('visitas').textContent=x.visitas;document.getElementById('estado').textContent='OK · 200';}catch{document.getElementById('estado').textContent='Sin conexión';}}
document.getElementById('saludar').addEventListener('click',async()=>{
 const name=document.getElementById('nombre').value;const el=document.getElementById('respuesta');
 try{const r=await fetch('/api/saludo?nombre='+encodeURIComponent(name));const v=await r.json();el.textContent=v.mensaje;}catch(e){el.textContent=e.message;}
});cargar();
