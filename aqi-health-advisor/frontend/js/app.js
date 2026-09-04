const Aero={
  key:'aero_user', profileKey:'aero_profile', coords:{lat:23.3315,lon:75.0367},
  saveUser(u){localStorage.setItem(this.key,JSON.stringify(u))},
  user(){try{return JSON.parse(localStorage.getItem(this.key)||'null')}catch{return null}},
  logout(){localStorage.removeItem(this.key);location.href='/login.html'},
  profile(){try{return JSON.parse(localStorage.getItem(this.profileKey)||'null')}catch{return null}},
  saveProfile(p){localStorage.setItem(this.profileKey,JSON.stringify(p))},
  async get(path){const r=await fetch(path);const d=await r.json();if(!r.ok)throw new Error(d.detail||'Request failed');return d},
  async post(path,body){const r=await fetch(path,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});const d=await r.json();if(!r.ok)throw new Error(d.detail||'Request failed');return d},
  weatherCode(code){if(code===0)return 'Clear'; if([1,2,3].includes(code))return 'Cloudy'; if([45,48].includes(code))return 'Fog'; if([51,53,55,56,57].includes(code))return 'Drizzle'; if([61,63,65,66,67,80,81,82].includes(code))return 'Rain'; if([71,73,75,77,85,86].includes(code))return 'Snow'; if([95,96,99].includes(code))return 'Thunderstorm'; return 'Weather'},
  weatherEmoji(code){if(code===0)return '☀️';if([1,2,3].includes(code))return '⛅';if([45,48].includes(code))return '🌫️';if([51,53,55,56,57].includes(code))return '🌦️';if([61,63,65,80,81,82].includes(code))return '🌧️';if([95,96,99].includes(code))return '⛈️';return '🌤️'},
  aqiState(v){if(v==null)return ['neutral','Unavailable'];if(v<=50)return ['good','Good'];if(v<=100)return ['moderate','Moderate'];if(v<=150)return ['poor','Unhealthy for sensitive groups'];return ['poor','Poor']},
  fmtDate(d){return new Date(d+'T12:00:00').toLocaleDateString('en-IN',{weekday:'short',day:'numeric',month:'short'})},
  async locate(){return new Promise(resolve=>{if(!navigator.geolocation)return resolve(this.coords);navigator.geolocation.getCurrentPosition(p=>{this.coords={lat:p.coords.latitude,lon:p.coords.longitude}},()=>{}, {enableHighAccuracy:true,timeout:5000});resolve(this.coords)})}
};
window.Aero=Aero;
function nav(){document.querySelectorAll('[data-nav]').forEach(a=>{if(a.dataset.nav===location.pathname.split('/').pop())a.classList.add('active')});const u=Aero.user();document.querySelectorAll('[data-user-name]').forEach(e=>e.textContent=u?.name||'Guest');document.querySelectorAll('[data-logout]').forEach(e=>e.onclick=()=>Aero.logout());document.querySelectorAll('[data-menu]').forEach(b=>b.onclick=()=>document.querySelector('.sidebar')?.classList.toggle('open'))}
function toast(t){const x=document.createElement('div');x.className='toast';x.textContent=t;document.body.appendChild(x);setTimeout(()=>x.remove(),2600)}
document.addEventListener('DOMContentLoaded',nav);window.toast=toast;
