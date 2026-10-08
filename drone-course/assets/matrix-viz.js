document.addEventListener('DOMContentLoaded',()=>{
  const configs={
    products:[['r','Độ dài r',0,.5,.01,.2,' m'],['f','Độ lớn F',0,10,.1,5,' N'],['angle','Góc α',-180,180,1,90,'°']],
    torque:[['rx','Vị trí rₓ',-.5,.5,.01,.2,' m'],['fz','Lực Fz',-10,10,.1,5,' N']],
    linear:[['case','Kiểu biến đổi',0,3,1,0,'']],
    rotation:[['roll','Roll φ',-90,90,1,0,'°'],['pitch','Pitch θ',-90,90,1,0,'°'],['yaw','Yaw ψ',-180,180,1,45,'°'],['vx','vᵇₓ',-2,2,.1,1,''],['vy','vᵇᵧ',-2,2,.1,0,''],['vz','vᵇ_z',-2,2,.1,0,'']],
    mixer:[['f1','M1 trước trái',0,5,.1,2.5,' N'],['f2','M2 trước phải',0,5,.1,2.5,' N'],['f3','M3 sau phải',0,5,.1,2.5,' N'],['f4','M4 sau trái',0,5,.1,2.5,' N']]
  };
  const fmt=(x,n=2)=>Math.abs(x)<1e-9?'0':x.toFixed(n);
  function arrow(ctx,a,b,color,width=3,dash=[]){
    const dx=b[0]-a[0],dy=b[1]-a[1],len=Math.hypot(dx,dy);if(len<2)return;
    ctx.save();ctx.strokeStyle=color;ctx.fillStyle=color;ctx.lineWidth=width;ctx.setLineDash(dash);ctx.beginPath();ctx.moveTo(...a);ctx.lineTo(...b);ctx.stroke();ctx.setLineDash([]);
    const h=Math.atan2(dy,dx),size=9+width;ctx.beginPath();ctx.moveTo(...b);ctx.lineTo(b[0]-size*Math.cos(h-.45),b[1]-size*Math.sin(h-.45));ctx.lineTo(b[0]-size*Math.cos(h+.45),b[1]-size*Math.sin(h+.45));ctx.closePath();ctx.fill();ctx.restore();
  }
  function line(ctx,a,b,color='#cbdce8',dash=[]){ctx.save();ctx.strokeStyle=color;ctx.lineWidth=1.3;ctx.setLineDash(dash);ctx.beginPath();ctx.moveTo(...a);ctx.lineTo(...b);ctx.stroke();ctx.restore()}
  function label(ctx,p,t,color='#34506b',size=15){ctx.fillStyle=color;ctx.font=`600 ${size}px system-ui`;ctx.fillText(t,p[0],p[1])}
  function products(ctx,s,out){
    const w=720,h=350,o=[345,205],angle=s.angle*Math.PI/180,rEnd=[o[0]+s.r*400,o[1]],fEnd=[o[0]+s.f*16*Math.cos(angle),o[1]-s.f*16*Math.sin(angle)];
    line(ctx,[45,o[1]],[675,o[1]],'#b8cad8');line(ctx,[o[0],42],[o[0],305],'#b8cad8');label(ctx,[660,o[1]-8],'x');label(ctx,[o[0]+8,50],'y');
    if(s.f>0){line(ctx,fEnd,[fEnd[0],o[1]],'#75a9b4',[6,5]);label(ctx,[fEnd[0]+7,o[1]+22],'F∥','#317981',13)}
    arrow(ctx,o,rEnd,'#d16a45',4);arrow(ctx,o,fEnd,'#08a69b',4);
    label(ctx,[rEnd[0]+8,rEnd[1]-10],'r','#ad5332');label(ctx,[fEnd[0]+8,fEnd[1]-7],'F','#147e75');
    ctx.beginPath();ctx.arc(o[0],o[1],5,0,Math.PI*2);ctx.fillStyle='#204b72';ctx.fill();
    const dot=s.r*s.f*Math.cos(angle),cross=s.r*s.f*Math.sin(angle);
    label(ctx,[55,292],`r · F = ${fmt(dot)} N·m`,'#204b72',17);
    label(ctx,[55,323],`(r × F)z = ${fmt(cross)} N·m`,'#204b72',17);
    label(ctx,[520,285],Math.abs(cross)<.001?'0':cross>0?'⊙ +z ra khỏi hình':'⊗ −z vào hình',cross>=0?'#2b70a7':'#a85a30',15);
    out.innerHTML=`<strong>Đầu ra khác loại:</strong> r·F = <strong>${fmt(dot)} N·m</strong> là số đo phần lực cùng hướng r. Nếu r là quãng dời s, cùng phép tính F·s cho công [J]. r×F = <strong>(0, 0, ${fmt(cross)}) N·m</strong> là vector mô-men; dấu cho biết chiều quay. Thử α=0° (mô-men bằng 0) và α=90° (tích vô hướng bằng 0).`;
  }
  function torque(ctx,s,out){
    const o=[340,235],r=[o[0]+s.rx*430,o[1]+s.rx*140],f=[r[0],r[1]-s.fz*17],tau=-s.rx*s.fz,t=[o[0]-tau*78,o[1]+tau*38];
    arrow(ctx,o,[555,305],'#d16a45',2);arrow(ctx,o,[165,325],'#259a82',2);arrow(ctx,o,[340,55],'#326db1',2);
    label(ctx,[560,317],'x / mũi','#a34d2e');label(ctx,[120,336],'y / trái','#16725f');label(ctx,[350,48],'z / lên','#285b99');
    line(ctx,r,[r[0],o[1]+s.rx*140],'#91a7b6',[5,5]);arrow(ctx,o,r,'#d16a45',5);arrow(ctx,r,f,'#08a69b',5);arrow(ctx,o,t,'#8b5aaa',4);
    ctx.beginPath();ctx.arc(o[0],o[1],7,0,Math.PI*2);ctx.fillStyle='#204b72';ctx.fill();
    label(ctx,[r[0]+8,r[1]+17],'r','#a34d2e');label(ctx,[f[0]+9,f[1]-6],'Fz','#127e73');label(ctx,[t[0]+8,t[1]-7],'τy','#784b9a');
    out.innerHTML=`<strong>Phép tính từ hình:</strong><span class="matrix-line">r=(${fmt(s.rx)},0,0) m; F=(0,0,${fmt(s.fz)}) N</span><span class="matrix-line">τ=r×F=(0,−rₓFz,0)=(0,${fmt(tau)},0) N·m</span>${Math.abs(tau)<1e-9?'Lực đi qua tâm hoặc bằng 0 nên không có mô-men.':tau<0?'Mô-men theo chiều −y: mũi drone có xu hướng ngẩng lên nếu chỉ tác dụng này.':'Mô-men theo chiều +y: mũi drone có xu hướng chúi xuống nếu chỉ tác dụng này.'}`;
  }
  function linear(ctx,s,out){
    const names=['Xoay 45°','Xô nghiêng','Phản xạ','Ép phẳng'],c=Math.SQRT1_2;
    const maps=[[[c,-c],[c,c]],[[1,.7],[0,1]],[[-1,0],[0,1]],[[1,0],[0,0]]],M=maps[s.case],det=M[0][0]*M[1][1]-M[0][1]*M[1][0];
    const apply=v=>[M[0][0]*v[0]+M[0][1]*v[1],M[1][0]*v[0]+M[1][1]*v[1]],origins=[[175,187],[540,187]],scale=58;
    origins.forEach((o,index)=>{
      const P=v=>[o[0]+v[0]*scale,o[1]-v[1]*scale],T=v=>index?apply(v):v;
      for(let j=-2;j<=2;j++){
        line(ctx,P(T([j,-2])),P(T([j,2])),'#dae7ef');
        line(ctx,P(T([-2,j])),P(T([2,j])),'#dae7ef');
      }
      const sq=[[0,0],[1,0],[1,1],[0,1]].map(v=>P(T(v)));ctx.beginPath();ctx.moveTo(...sq[0]);sq.slice(1).forEach(p=>ctx.lineTo(...p));ctx.closePath();ctx.fillStyle='rgba(117,75,162,.18)';ctx.fill();ctx.strokeStyle='#754ba2';ctx.lineWidth=2.5;ctx.stroke();
      arrow(ctx,o,P(T([1,0])),'#d16a45',4);arrow(ctx,o,P(T([0,1])),'#259a82',4);
      label(ctx,[o[0]-65,42],index?'Sau: A biến đổi':'Trước: I giữ nguyên','#204b72',17);
      label(ctx,[P(T([1,0]))[0]+6,P(T([1,0]))[1]-8],'cột 1','#a34d2e',13);
      label(ctx,[P(T([0,1]))[0]+6,P(T([0,1]))[1]-8],'cột 2','#16725f',13);
    });
    arrow(ctx,[338,187],[383,187],'#d47a2c',3);label(ctx,[351,175],'A','#b26525',16);
    const meaning=s.case===0?'Chỉ xoay: diện tích và chiều tay không đổi.':s.case===1?'Xô nghiêng: hình dạng đổi, diện tích vẫn giữ.':s.case===2?'Gương đảo tay hệ trục: không thể tạo bằng phép quay 3D.':'Hai trục cùng nằm trên một đường: mất chiều y, không thể khôi phục tọa độ ban đầu.';
    out.innerHTML=`<strong>${names[s.case]}</strong><span class="matrix-line">A = [[${fmt(M[0][0])}, ${fmt(M[0][1])}], [${fmt(M[1][0])}, ${fmt(M[1][1])}]]</span><span class="matrix-line">det(A) = ${fmt(det)}; hạng = ${s.case===3?1:2}</span>${meaning} ${Math.abs(det)<1e-9?'Det=0 nên không có nghịch đảo.':'Det≠0 nên có phép biến đổi ngược.'}`;
  }
  function rotate(v,s){
    const r=s.roll*Math.PI/180,p=s.pitch*Math.PI/180,y=s.yaw*Math.PI/180;
    let [x,yy,z]=v;[yy,z]=[yy*Math.cos(r)-z*Math.sin(r),yy*Math.sin(r)+z*Math.cos(r)];
    [x,z]=[x*Math.cos(p)+z*Math.sin(p),-x*Math.sin(p)+z*Math.cos(p)];
    [x,yy]=[x*Math.cos(y)-yy*Math.sin(y),x*Math.sin(y)+yy*Math.cos(y)];return [x,yy,z];
  }
  function rotation(ctx,s,out){
    const o=[355,233],P=v=>[o[0]+100*(.85*v[0]-.85*v[1]),o[1]+100*(.43*v[0]+.43*v[1]-.9*v[2])];
    const basis=[[1,0,0],[0,1,0],[0,0,1]],colors=['#d16a45','#259a82','#326db1'],cols=basis.map(v=>rotate(v,s)),v=[s.vx,s.vy,s.vz],world=rotate(v,s);
    basis.forEach((e,i)=>{arrow(ctx,o,P(e.map(x=>x*1.65)),'#b9cbd9',2);label(ctx,P(e.map(x=>x*1.7)),['xʷ','yʷ','zʷ'][i],'#71869a',13)});
    cols.forEach((e,i)=>{arrow(ctx,o,P(e.map(x=>x*1.1)),colors[i],3);label(ctx,P(e.map(x=>x*1.18)),['xᵇ','yᵇ','zᵇ'][i],colors[i],14)});
    arrow(ctx,o,P(v),'#98a6b2',2,[5,5]);arrow(ctx,o,P(world),'#754ba2',5);
    label(ctx,[P(world)[0]+8,P(world)[1]-8],'Rvᵇ','#754ba2',15);
    label(ctx,[35,45],'Nét xám đứt: hướng khi R = I','#52677d',14);
    label(ctx,[35,70],'Tím: vector khi thân đã quay','#754ba2',14);
    const row=i=>cols.map(c=>fmt(c[i])).join(', ');
    out.innerHTML=`<strong>R biến tọa độ body → world.</strong><span class="matrix-line">R = [[${row(0)}], [${row(1)}], [${row(2)}]]</span><span class="matrix-line">vᵇ = (${fmt(s.vx)}, ${fmt(s.vy)}, ${fmt(s.vz)})</span><span class="matrix-line">vʷ = Rvᵇ = (${fmt(world[0])}, ${fmt(world[1])}, ${fmt(world[2])})</span>Mỗi cột màu của R là một trục thân viết trong world. Nhân từng tọa độ vᵇ với cột tương ứng rồi cộng ba mũi tên. Rᵀ đổi ngược world → body.`;
  }
  function mixer(ctx,s,out){
    const o=[350,175],pos=[[235,62],[465,62],[465,285],[235,285]],fs=[s.f1,s.f2,s.f3,s.f4],a=.18,gamma=.02;
    pos.forEach((p,i)=>{line(ctx,o,p,'#7193ad');ctx.beginPath();ctx.arc(p[0],p[1],26+fs[i]*3,0,Math.PI*2);ctx.fillStyle=`rgba(8,166,155,${.13+fs[i]*.11})`;ctx.fill();ctx.strokeStyle='#28719f';ctx.lineWidth=2;ctx.stroke();label(ctx,[p[0]-19,p[1]+5],`M${i+1}`,'#204b72',17);label(ctx,[p[0]-30,p[1]+55],`${fmt(fs[i],1)} N`,'#145f6e',14)});
    ctx.beginPath();ctx.arc(o[0],o[1],26,0,Math.PI*2);ctx.fillStyle='#204b72';ctx.fill();label(ctx,[o[0]-13,o[1]+5],'CG','#fff',14);
    arrow(ctx,[90,255],[90,175],'#d16a45',3);arrow(ctx,[90,255],[35,255],'#259a82',3);label(ctx,[103,177],'x / mũi','#a34d2e');label(ctx,[15,281],'y / trái','#16725f');
    const T=fs.reduce((u,x)=>u+x,0),tx=a*(fs[0]-fs[1]-fs[2]+fs[3]),ty=a*(-fs[0]-fs[1]+fs[2]+fs[3]),tz=gamma*(-fs[0]+fs[1]-fs[2]+fs[3]);
    out.innerHTML=`<strong>u = M f</strong><span class="matrix-line">f = (${fs.map(x=>fmt(x,1)).join(', ')}) N</span><span class="matrix-line">T = ${fmt(T)} N</span><span class="matrix-line">τx = ${fmt(tx)}; τy = ${fmt(ty)}; τz = ${fmt(tz)} N·m</span><strong>Đọc cột M1:</strong> tăng riêng F₁ thêm 1 N làm T tăng 1 N, τx tăng ${a} N·m, τy giảm ${a} N·m, τz giảm ${gamma} N·m. Thử tăng riêng một motor rồi tăng đều bốn motor.`;
  }
  const drawers={products,torque,linear,rotation,mixer};
  document.querySelectorAll('[data-matrix-demo]').forEach(root=>{
    const type=root.dataset.matrixDemo,scene=root.querySelector('[data-scene]'),ctx=scene.getContext('2d'),controls=root.querySelector('[data-controls]'),out=root.querySelector('[data-result]'),state={};
    const render=()=>{ctx.clearRect(0,0,scene.width,scene.height);drawers[type](ctx,state,out)};
    configs[type].forEach(([key,name,min,max,step,initial,unit])=>{
      state[key]=initial;const labelEl=document.createElement('label'),row=document.createElement('span'),title=document.createElement('span'),value=document.createElement('strong'),input=document.createElement('input');
      title.textContent=name;value.textContent=type==='linear'?['Xoay','Xô nghiêng','Phản xạ','Ép phẳng'][initial]:initial+unit;row.append(title,value);input.type='range';input.min=min;input.max=max;input.step=step;input.value=initial;input.setAttribute('aria-label',name);
      input.addEventListener('input',()=>{state[key]=Number(input.value);value.textContent=type==='linear'?['Xoay','Xô nghiêng','Phản xạ','Ép phẳng'][state[key]]:state[key]+unit;render()});labelEl.append(row,input);controls.append(labelEl);
    });render();
  });
});
