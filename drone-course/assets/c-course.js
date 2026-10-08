document.addEventListener('DOMContentLoaded',()=>{
  const demos=document.querySelectorAll('[data-c-demo]');
  const spec={
    sensor:[
      ['tilt','Roll thật',-60,60,1,20,'°'],['lateral','Gia tốc ngang',-6,6,.1,0,' m/s²'],
      ['bias','Bias gyro',-3,3,.1,.5,' °/s'],['seconds','Thời gian tích phân',1,30,1,12,' s']],
    fusion:[
      ['bias','Bias gyro',-3,3,.1,1,' °/s'],['noise','Nhiễu accel',0,8,.2,2,'°'],
      ['burst','Gia tốc trong 3–5 s',0,24,1,14,'°'],['tau','Hằng số τ',.2,5,.1,1,' s']],
    loop:[
      ['target','Roll mục tiêu',-30,30,1,15,'°'],['bias','Bias gyro',-3,3,.1,1,' °/s'],
      ['delay','Trễ motor',.02,.45,.01,.08,' s'],['mode','Nguồn góc','select',['fusion','gyro'],'fusion','']],
    safety:[
      ['mass','Khối lượng drone',.3,3,.1,1,' kg'],['thrust','Thrust tối đa / rotor',1,15,.1,5,' N'],
      ['imu','IMU hợp lệ','check',true],['estimate','Estimator hợp lệ','check',true],
      ['link','Lệnh điều khiển còn mới','check',true],['battery','Pin trong giới hạn','check',true]]
  };
  function createControl(root,item,state,render){
    const [key,name,min,max,step,initial,unit]=item;
    const label=document.createElement('label');const row=document.createElement('span');
    const title=document.createElement('span');title.textContent=name;row.append(title);
    let input,value;
    if(min==='check'){
      input=document.createElement('input');input.type='checkbox';input.checked=max;state[key]=max;
      label.prepend(input);label.append(title);
    }else if(min==='select'){
      input=document.createElement('select');for(const option of max){const el=document.createElement('option');el.value=option;el.textContent=option==='fusion'?'Complementary filter':'Chỉ tích phân gyro';input.append(el)}
      input.value=step;state[key]=step;label.append(row,input);
    }else{
      value=document.createElement('strong');row.append(value);input=document.createElement('input');input.type='range';
      input.min=min;input.max=max;input.step=step;input.value=initial;state[key]=initial;label.append(row,input);
      value.textContent=initial+unit;
    }
    input.setAttribute('aria-label',name);
    input.addEventListener('input',()=>{state[key]=input.type==='checkbox'?input.checked:input.type==='range'?Number(input.value):input.value;if(value)value.textContent=state[key]+unit;render()});
    root.append(label);
  }
  function plot(canvas,series,yMin,yMax,xMax){
    const ctx=canvas.getContext('2d'),w=canvas.width,h=canvas.height;
    const left=43,right=w-14,top=35,bottom=h-35;
    ctx.clearRect(0,0,w,h);ctx.fillStyle='#fbfdff';ctx.fillRect(0,0,w,h);
    const px=x=>left+(x/xMax)*(right-left),py=y=>bottom-(y-yMin)/(yMax-yMin)*(bottom-top);
    ctx.font='12px system-ui';ctx.textAlign='right';ctx.textBaseline='middle';
    for(let i=0;i<=4;i++){const y=yMin+(yMax-yMin)*i/4,yp=py(y);ctx.strokeStyle='#deebf3';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(left,yp);ctx.lineTo(right,yp);ctx.stroke();ctx.fillStyle='#61778b';ctx.fillText(y.toFixed(0)+'°',left-7,yp)}
    for(let i=0;i<=4;i++){const x=xMax*i/4,xp=px(x);ctx.strokeStyle='#e8eff5';ctx.beginPath();ctx.moveTo(xp,top);ctx.lineTo(xp,bottom);ctx.stroke();ctx.fillStyle='#61778b';ctx.textAlign='center';ctx.fillText(x.toFixed(0)+' s',xp,bottom+16)}
    let legendX=left+8;ctx.textBaseline='middle';
    for(const s of series){ctx.fillStyle=s.color;ctx.fillRect(legendX,10,16,3);ctx.textAlign='left';ctx.fillText(s.name,legendX+21,12);legendX+=Math.min(170,44+s.name.length*8)}
    for(const s of series){ctx.strokeStyle=s.color;ctx.lineWidth=s.width||2.5;ctx.beginPath();s.points.forEach((p,i)=>{if(i===0)ctx.moveTo(px(p[0]),py(p[1]));else ctx.lineTo(px(p[0]),py(p[1]))});ctx.stroke()}
  }
  function sensor(root,s,canvas,result){
    const g=9.81,truth=s.tilt,fy=g*Math.sin(truth*Math.PI/180)+s.lateral,fz=g*Math.cos(truth*Math.PI/180),acc=Math.atan2(fy,fz)*180/Math.PI;
    const series=[{name:'Roll thật',color:'#204b72',points:[]},{name:'Từ accel',color:'#08a69b',points:[]},{name:'Gyro tích phân',color:'#d47a2c',points:[]}];
    for(let i=0;i<=100;i++){const t=s.seconds*i/100;series[0].points.push([t,truth]);series[1].points.push([t,acc]);series[2].points.push([t,truth+s.bias*t])}
    const ymin=Math.min(truth,acc,truth+s.bias*s.seconds)-10,ymax=Math.max(truth,acc,truth+s.bias*s.seconds)+10;
    plot(canvas,series,ymin,ymax,s.seconds);
    result.textContent=`Góc thật ${truth.toFixed(1)}°; accelerometer suy ra ${acc.toFixed(1)}° (sai ${(acc-truth).toFixed(1)}°); gyro tích phân sau ${s.seconds} s là ${(truth+s.bias*s.seconds).toFixed(1)}° (trôi ${(s.bias*s.seconds).toFixed(1)}°). Mô hình giữ roll thật cố định để cô lập hai nguồn sai số.`;
  }
  function fusion(root,s,canvas,result){
    const dt=.02,total=12,alpha=s.tau/(s.tau+dt),lines=[
      {name:'Roll thật',color:'#204b72',points:[]},{name:'Accel',color:'#74ae93',points:[]},
      {name:'Gyro tích phân',color:'#d47a2c',points:[]},{name:'Fusion',color:'#1681b7',points:[],width:3.2}];
    let gyro=0,estimate=0,errGyro=0,errFusion=0,count=0;
    for(let i=0;i<=total/dt;i++){
      const t=i*dt,truth=18*Math.sin(.75*t),rate=13.5*Math.cos(.75*t),gyroMeasure=rate+s.bias+.18*Math.sin(15*t);
      const disturbance=t>=3&&t<=5?s.burst:0,acc=truth+disturbance+s.noise*(.55*Math.sin(19*t)+.45*Math.sin(31*t));
      if(i){gyro+=gyroMeasure*dt;estimate=alpha*(estimate+gyroMeasure*dt)+(1-alpha)*acc}
      if(i%3===0){lines[0].points.push([t,truth]);lines[1].points.push([t,acc]);lines[2].points.push([t,gyro]);lines[3].points.push([t,estimate])}
      if(i&&t>5){errGyro+=Math.abs(gyro-truth);errFusion+=Math.abs(estimate-truth);count++}
    }
    plot(canvas,lines,-35,45,total);
    result.textContent=`Sau đoạn nhiễu 3–5 s, sai số tuyệt đối trung bình: gyro ${(errGyro/count).toFixed(1)}°, fusion ${(errFusion/count).toFixed(1)}°. α = ${alpha.toFixed(3)} mỗi mẫu 20 ms. Đây là bộ lọc roll một trục, chưa phải estimator quaternion 3D.`;
  }
  function loop(root,s,canvas,result){
    const dt=.01,total=8,J=.025,damping=.03,limit=.12;
    let angle=0,rate=0,estimate=0,motor=0,saturated=0,peak=0;
    const lines=[{name:'Mục tiêu',color:'#52677d',points:[]},{name:'Roll thật',color:'#204b72',points:[],width:3},{name:'Ước lượng',color:'#08a69b',points:[]}];
    for(let i=0;i<=total/dt;i++){
      const t=i*dt,target=t>=.5?s.target:0,gyro=rate+s.bias,acc=angle+.6*Math.sin(17*t);
      estimate+=gyro*dt;if(s.mode==='fusion')estimate=(1-dt/1.2)*estimate+(dt/1.2)*acc;
      const rateSp=Math.max(-120,Math.min(120,3*(target-estimate)));
      const requested=.0025*(rateSp-gyro),command=Math.max(-limit,Math.min(limit,requested));
      if(Math.abs(requested)>limit)saturated++;
      motor+=(command-motor)*dt/s.delay;
      const accel=(motor-damping*rate*Math.PI/180)/J*180/Math.PI;
      rate+=accel*dt;angle+=rate*dt;
      if(t>.5)peak=Math.max(peak,Math.abs(angle));
      if(i%3===0){lines[0].points.push([t,target]);lines[1].points.push([t,angle]);lines[2].points.push([t,estimate])}
    }
    const bound=Math.max(35,Math.ceil((Math.max(Math.abs(s.target),peak)+10)/10)*10);
    plot(canvas,lines,-bound,bound,total);
    result.textContent=`Cuối 8 s: roll thật ${angle.toFixed(1)}°, ước lượng ${estimate.toFixed(1)}°; mô-men yêu cầu bị kẹp ${(100*saturated/(total/dt+1)).toFixed(1)}% mẫu. Tăng trễ motor hoặc dùng gyro lệch bias để quan sát sai số và dao động.`;
  }
  function safety(root,s,visual,result,flight){
    const ratio=4*s.thrust/(s.mass*9.81),hover=s.mass*9.81/(4*s.thrust)*100;
    const missing=[];if(!s.imu)missing.push('IMU');if(!s.estimate)missing.push('estimator');if(!s.link)missing.push('lệnh điều khiển');if(!s.battery)missing.push('pin');
    const ready=missing.length===0&&ratio>=1.5;
    if(flight.armed&&!ready){flight.armed=false;flight.failsafe=true}
    const status=flight.failsafe?'FAILSAFE':flight.armed?'ARMED':ready?'SẴN SÀNG ARM':'KHÓA ARM';
    visual.innerHTML=`<div class="c-safety-bar" style="--hover:${Math.min(100,hover).toFixed(1)}%" aria-label="Tỷ lệ thrust hover trên thrust tối đa"><span style="width:${Math.min(100,hover).toFixed(1)}%"></span></div><div><strong>Thrust hover / rotor:</strong> ${(s.mass*9.81/4).toFixed(2)} N · <strong>dư địa:</strong> ${ratio.toFixed(2)}× · <strong>mức hover:</strong> ${hover.toFixed(0)}% thrust tối đa</div><div><span class="c-status ${ready&&!flight.failsafe?'':'bad'}">${status}</span> <button type="button" data-arm>${flight.failsafe?'Xóa lỗi':flight.armed?'Disarm':'Thử arm'}</button></div>`;
    visual.querySelector('[data-arm]').addEventListener('click',()=>{if(flight.failsafe)flight.failsafe=false;else if(flight.armed)flight.armed=false;else if(ready)flight.armed=true;safety(root,s,visual,result,flight)});
    result.textContent=flight.failsafe?'Điều kiện hợp lệ mất trong lúc ARMED: mô phỏng chuyển FAILSAFE và chặn lệnh arm cho đến khi kiểm tra lại.':
      missing.length?'Chưa đạt precheck: '+missing.join(', ')+'.':ratio<1?'Tổng lực tối đa nhỏ hơn trọng lượng: không thể hover.':ratio<1.5?'Dư địa dưới ngưỡng minh họa 1,5×: cần xem lại cấu hình và điện áp tải.':
      flight.armed?'Mô phỏng đang ARMED. Tắt một điều kiện để xem phản ứng lỗi.':'Các điều kiện minh họa đã đạt; bấm “Thử arm” để kiểm tra chuyển trạng thái.';
  }
  demos.forEach(root=>{
    const type=root.dataset.cDemo,s={},controls=root.querySelector('[data-controls]'),canvas=root.querySelector('[data-chart]'),visual=root.querySelector('[data-visual]'),result=root.querySelector('[data-result]'),flight={armed:false,failsafe:false};
    const render=()=>({sensor:()=>sensor(root,s,canvas,result),fusion:()=>fusion(root,s,canvas,result),loop:()=>loop(root,s,canvas,result),safety:()=>safety(root,s,visual,result,flight)})[type]();
    spec[type].forEach(item=>createControl(controls,item,s,render));render();
  });
});
