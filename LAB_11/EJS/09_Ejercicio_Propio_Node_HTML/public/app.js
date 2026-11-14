const KEY='pizarra_sesion10_v1';
function get(){try{return JSON.parse(localStorage.getItem(KEY)||'[]').filter(t=>t&&typeof t.titulo==='string')}catch{return []}}
let tareas=get();
const store=()=>localStorage.setItem(KEY,JSON.stringify(tareas));
function pintar(){const grid=document.getElementById('pizarra');grid.replaceChildren();
 document.getElementById('total').textContent=tareas.length;document.getElementById('finalizadas').textContent=tareas.filter(t=>t.hecha).length;
 if(!tareas.length){const el=document.createElement('div');el.className='empty wide';el.textContent='Pizarra vacía. Crea tu primera tarea.';grid.append(el);return}
 for(const t of tareas){const card=document.createElement('article');card.className='card';
 const over=document.createElement('div');over.className='overline';over.textContent=t.prioridad+' · '+(t.hecha?'FINALIZADA':'PENDIENTE');
 const h=document.createElement('h2');h.textContent=t.titulo;if(t.hecha)h.style.textDecoration='line-through';
 const buttons=document.createElement('div');buttons.className='row';
 const done=document.createElement('button');done.className='btn secondary';done.textContent=t.hecha?'Reabrir':'Completar';done.addEventListener('click',()=>{t.hecha=!t.hecha;store();pintar()});
 const del=document.createElement('button');del.className='filter';del.textContent='Eliminar';del.addEventListener('click',()=>{tareas=tareas.filter(x=>x.id!==t.id);store();pintar()});
 buttons.append(done,del);card.append(over,h,buttons);grid.append(card);
 }
}
document.getElementById('form').addEventListener('submit',e=>{e.preventDefault();const inp=document.getElementById('titulo');const titulo=inp.value.trim();if(!titulo)return;
 tareas.unshift({id:crypto.randomUUID?crypto.randomUUID():String(Date.now()+Math.random()),titulo,prioridad:document.getElementById('prioridad').value,hecha:false});store();inp.value='';pintar();inp.focus()});
pintar();
