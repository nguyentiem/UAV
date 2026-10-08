document.addEventListener('DOMContentLoaded',()=>{
  const canvas=document.getElementById('six-dof-canvas');
  if(!canvas)return;
  const ctx=canvas.getContext('2d');
  const controls=document.getElementById('six-dof-controls');
  const readout=document.getElementById('six-dof-readout');
  const specs=[
    {key:'x',name:'x · Đông',min:-1.5,max:1.5,step:.1,unit:' m'},
    {key:'y',name:'y · Bắc',min:-1.5,max:1.5,step:.1,unit:' m'},
    {key:'z',name:'z · độ cao',min:-.7,max:1.5,step:.1,unit:' m'},
    {key:'roll',name:'Roll φ · quanh trục mũi',min:-60,max:60,step:1,unit:'°'},
    {key:'pitch',name:'Pitch θ · quanh trục trái',min:-60,max:60,step:1,unit:'°'},
    {key:'yaw',name:'Yaw ψ · quanh trục lên',min:-180,max:180,step:1,unit:'°'}
  ];
  const state={x:0,y:0,z:0,roll:0,pitch:0,yaw:0};
  let azimuth=Math.PI/4,elevation=.62,active='x',width=0,height=0;
  const inputs={};
  specs.forEach(s=>{
    const label=document.createElement('label');label.className='six-dof-control';
    const head=document.createElement('span');
    const title=document.createElement('span');title.textContent=s.name;
    const value=document.createElement('strong');value.textContent='0'+s.unit;
    head.append(title,value);
    const input=document.createElement('input');input.type='range';input.min=s.min;input.max=s.max;input.step=s.step;input.value=0;input.setAttribute('aria-label',s.name);
    input.addEventListener('input',()=>{state[s.key]=Number(input.value);value.textContent=(state[s.key]>0?'+':'')+state[s.key]+s.unit;active=s.key;update()});
    label.append(head,input);controls.append(label);inputs[s.key]={input,value,unit:s.unit};
  });
  document.getElementById('six-dof-reset').addEventListener('click',()=>{
    specs.forEach(s=>{state[s.key]=0;inputs[s.key].input.value=0;inputs[s.key].value.textContent='0'+s.unit});
    active='x';update();
  });
  const descriptions={
    x:v=>v===0?'Tâm drone ở vị trí x ban đầu.':v>0?'Drone dịch về Đông theo trục x thế giới.':'Drone dịch về Tây, ngược chiều trục x thế giới.',
    y:v=>v===0?'Tâm drone ở vị trí y ban đầu.':v>0?'Drone dịch về Bắc theo trục y thế giới.':'Drone dịch về Nam, ngược chiều trục y thế giới.',
    z:v=>v===0?'Drone ở độ cao tham chiếu 1,0 m.':v>0?'Drone cao hơn vị trí tham chiếu.':'Drone thấp hơn vị trí tham chiếu.',
    roll:v=>v===0?'Hai bên drone đang ngang nhau.':v>0?'Roll dương: bên trái nâng lên, bên phải hạ xuống.':'Roll âm: bên trái hạ xuống, bên phải nâng lên.',
    pitch:v=>v===0?'Mũi và đuôi drone đang ngang nhau.':v>0?'Pitch dương: mũi chúi xuống, đuôi nâng lên.':'Pitch âm: mũi ngẩng lên, đuôi hạ xuống.',
    yaw:v=>v===0?'Mũi drone hướng theo trục x thế giới.':v>0?'Yaw dương: mũi quay về phía trục y (trái khi nhìn từ trên).':'Yaw âm: mũi quay khỏi trục y (phải khi nhìn từ trên).'
  };
  function update(){
    readout.textContent=descriptions[active](state[active])+' Vị trí tâm: ('+state.x.toFixed(1)+', '+state.y.toFixed(1)+', '+(1+state.z).toFixed(1)+') m; roll '+state.roll+'°, pitch '+state.pitch+'°, yaw '+state.yaw+'°.';
    draw();
  }
  function rotate(v){
    const r=state.roll*Math.PI/180,p=state.pitch*Math.PI/180,y=state.yaw*Math.PI/180;
    let [x,yy,z]=v;
    [yy,z]=[yy*Math.cos(r)-z*Math.sin(r),yy*Math.sin(r)+z*Math.cos(r)];
    [x,z]=[x*Math.cos(p)+z*Math.sin(p),-x*Math.sin(p)+z*Math.cos(p)];
    [x,yy]=[x*Math.cos(y)-yy*Math.sin(y),x*Math.sin(y)+yy*Math.cos(y)];
    return [x+state.x,yy+state.y,z+1+state.z];
  }
  function project(v){
    const scale=Math.min(width/7.3,height/5.1);
    return [width/2+scale*(Math.cos(azimuth)*v[0]-Math.sin(azimuth)*v[1]),
      height*.64+scale*(Math.sin(elevation)*(Math.sin(azimuth)*v[0]+Math.cos(azimuth)*v[1])-Math.cos(elevation)*v[2])];
  }
  function line(a,b,color,size=2,dash=[]){
    const p=project(a),q=project(b);ctx.beginPath();ctx.setLineDash(dash);ctx.moveTo(...p);ctx.lineTo(...q);ctx.strokeStyle=color;ctx.lineWidth=size;ctx.stroke();ctx.setLineDash([]);
  }
  function dot(v,r,fill){const p=project(v);ctx.beginPath();ctx.arc(p[0],p[1],r,0,Math.PI*2);ctx.fillStyle=fill;ctx.fill()}
  function label(v,t,color){const p=project(v);ctx.font='bold 13px system-ui';ctx.fillStyle=color;ctx.fillText(t,p[0]+5,p[1]-5)}
  function ring(center,r,color){
    ctx.beginPath();for(let i=0;i<=32;i++){
      const a=i*Math.PI/16,p=project(rotate([center[0]+r*Math.cos(a),center[1]+r*Math.sin(a),center[2]]));
      if(i===0)ctx.moveTo(...p);else ctx.lineTo(...p);
    }ctx.fillStyle='rgba(120,193,216,.23)';ctx.fill();ctx.strokeStyle=color;ctx.lineWidth=2;ctx.stroke();
  }
  function draw(){
    if(!width)return;
    ctx.clearRect(0,0,width,height);
    for(let i=-2;i<=2;i+=.5){line([i,-2,0],[i,2,0],'#d8e7ee',1);line([-2,i,0],[2,i,0],'#d8e7ee',1)}
    line([-2,0,0],[2.25,0,0],'#d16a45',2.5);line([0,-2,0],[0,2.25,0],'#259a82',2.5);line([0,0,0],[0,0,2.1],'#326db1',2.5);
    label([2.25,0,0],'x · Đông','#a34d2e');label([0,2.25,0],'y · Bắc','#16725f');label([0,0,2.1],'z · lên','#285b99');
    const center=rotate([0,0,0]),ground=[state.x,state.y,0];
    dot(ground,17,'rgba(30,69,102,.12)');line(ground,center,'#8daabd',1.5,[5,4]);
    const motors=[[-.7,.7,0],[.7,.7,0],[-.7,-.7,0],[.7,-.7,0]];
    motors.forEach(m=>line(center,rotate(m),'#527897',11));
    motors.forEach(m=>{ring(m,.24,'#38849e');dot(rotate(m),5,'#24577b')});
    dot(center,17,'#244f73');dot(rotate([.2,0,.04]),5,'#f2a356');
    line(center,rotate([1.02,0,0]),'#d16a45',3);label(rotate([1.02,0,0]),'mũi / xᵇ','#a34d2e');
    line(center,rotate([0,1.02,0]),'#259a82',3);label(rotate([0,1.02,0]),'trái / yᵇ','#16725f');
    line(center,rotate([0,0,.88]),'#326db1',3);label(rotate([0,0,.88]),'zᵇ','#285b99');
  }
  function resize(){const rect=canvas.getBoundingClientRect(),ratio=window.devicePixelRatio||1;width=rect.width;height=rect.height;canvas.width=Math.round(width*ratio);canvas.height=Math.round(height*ratio);ctx.setTransform(ratio,0,0,ratio,0,0);draw()}
  if(window.ResizeObserver)new ResizeObserver(resize).observe(canvas);else window.addEventListener('resize',resize);
  let pointer=null;
  canvas.addEventListener('pointerdown',e=>{pointer={id:e.pointerId,x:e.clientX,y:e.clientY};canvas.setPointerCapture(e.pointerId)});
  canvas.addEventListener('pointermove',e=>{if(!pointer||pointer.id!==e.pointerId)return;azimuth+=(e.clientX-pointer.x)*.008;elevation=Math.max(.2,Math.min(1.25,elevation+(e.clientY-pointer.y)*.006));pointer.x=e.clientX;pointer.y=e.clientY;draw()});
  canvas.addEventListener('pointerup',()=>{pointer=null});canvas.addEventListener('pointercancel',()=>{pointer=null});
  resize();update();
});
