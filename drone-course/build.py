from pathlib import Path
from html import escape

ROOT=Path(__file__).parent
LESSONS=[]
def add(num,title,group,lead,goals,sections,diagram,caption,practice,checks,demo=''):
    LESSONS.append(dict(num=num,title=title,group=group,lead=lead,goals=goals,sections=sections,diagram=diagram,caption=caption,practice=practice,checks=checks,demo=demo))

add(1,'Tổng quan bài toán','A1 · Toán công cụ',
'Một quadcopter điều khiển sáu tọa độ chuyển động bằng bốn tốc độ motor. Bài này dựng bản đồ để bạn biết mỗi công thức sau này giải quyết phần nào.',
['Phân biệt 6 bậc tự do với 4 đầu vào điều khiển','Giải thích chuỗi motor → lực/mô-men → gia tốc → chuyển động','Nhìn thấy mối liên hệ giữa 15 bài của Phần A'],[
('Sáu bậc tự do là gì?','<p>Vị trí gồm ba tọa độ x, y, z. Tư thế gồm ba góc roll φ (nghiêng trái/phải quanh trục x), pitch θ (chúi/ngẩng quanh trục y), yaw ψ (đổi hướng quanh trục z). Trạng thái chuyển động còn cần vận tốc thẳng và vận tốc góc. “6-DOF” đếm các hướng chuyển động độc lập về hình học, không có nghĩa ta có sáu nút điều khiển độc lập.</p><div class="concept">Ví dụ: muốn bay ngang, drone phải nghiêng để lực đẩy của cánh quạt có thành phần nằm ngang. Vì thế thay đổi vị trí x/y kéo theo thay đổi tư thế.</div>'),
('Bốn motor thực sự điều khiển gì?','<p>Mỗi cánh quạt tạo lực đẩy gần theo trục z của thân. Chênh lệch lực giữa các motor tạo mô-men roll, pitch. Chênh lệch mô-men phản lực của hai nhóm quay ngược chiều tạo yaw. Ta gộp bốn tác động thành <strong>tổng lực đẩy T và ba mô-men τx, τy, τz</strong>.</p><div class="formula">[ω₁, ω₂, ω₃, ω₄] → [T, τx, τy, τz] → [r̈, ω̇] → [r, R]</div><p>Motor không ra lệnh trực tiếp cho tọa độ x. Bộ điều khiển phải tính lực cần thiết, chọn tư thế phù hợp rồi phân bổ lệnh cho bốn motor. Đây là lý do quadcopter là hệ <strong>thiếu chấp hành</strong>.</p>'),
('Bản đồ kiến thức','<ol class="steps"><li>A2–A5: vector, đạo hàm và hệ trục để viết chuyển động 3D.</li><li>A6–A7: Newton và vật rắn để đổi lực/mô-men thành gia tốc.</li><li>A8–A12: không khí, cánh quạt, motor và pin để đổi lệnh điện thành lực.</li><li>A13: ghép tất cả thành phương trình Newton–Euler.</li><li>A14–A15: tuyến tính hóa, mô phỏng và kiểm tra dự đoán.</li></ol><p>Các phần cảm biến và điều khiển của tài liệu nguồn nằm sau mô hình vật lý này.</p>')],
'drone','Drone nhìn từ trên: bốn rotor quanh tâm khối lượng; mũi ở phía trên hình.',
'Vẽ drone nhìn từ trên và từ cạnh. Ghi rõ bốn motor, tâm khối lượng, T và mg. Dự đoán điều gì xảy ra nếu tăng đều bốn motor.',
['Vì sao drone cần nghiêng khi muốn bay ngang?','Tại sao 6-DOF không đồng nghĩa với 6 motor?'],'hover')

add(2,'Đại số tuyến tính cho cơ học bay','A1 · Toán công cụ',
'Vector và ma trận là ngôn ngữ để nói lực tác dụng ở đâu, hướng nào và được đổi giữa các hệ tọa độ ra sao.',
['Tính được mô-men r × F','Hiểu định thức, hạng, nghịch đảo và trị riêng','Kiểm tra một ma trận có phải phép xoay hợp lệ'],[
('Vector và hai phép nhân','<p>Vector có độ lớn và hướng. Tích vô hướng a·b = |a||b|cosα đo mức cùng hướng, ví dụ công W = F·s. Tích có hướng a×b vuông góc với cả hai vector, có độ lớn |a||b|sinα; chiều theo quy tắc bàn tay phải. Với cánh tay đòn r từ khối tâm tới điểm đặt lực, <strong>τ = r×F</strong>.</p><div class="formula">r = (0,20; 0; 0) m, F = (0; 0; 5) N ⇒ τ = (0; −1; 0) N·m</div><p>Dấu âm nói mô-men quanh trục y theo chiều âm; lực 5 N đặt đúng tâm sẽ cho r=0 và không tạo mô-men.</p>'),
('Ma trận, định thức và hạng','<p>Ma trận nhân vector để biến đổi tọa độ hoặc ghép các đầu vào. Nhân ma trận là “đầu ra của phép này trở thành đầu vào của phép kia”, nên thứ tự thường không đổi được: AB ≠ BA. Ma trận vuông có nghịch đảo chỉ khi định thức khác 0. Hạng cho biết số hàng/cột độc lập; mixer có hạng 4 mới phân biệt được bốn yêu cầu T, roll, pitch, yaw.</p><p>Trị riêng λ và vector riêng v thỏa Av=λv: tác động của A lên v chỉ đổi độ lớn hoặc đảo chiều. Với tensor quán tính J đối xứng, các vector riêng là trục chính; với mô hình tuyến tính ẋ=Ax, phần thực của trị riêng giúp đánh giá xu hướng tăng/giảm của nhiễu động.</p>'),
('Ma trận xoay và tích có hướng dạng ma trận','<p>Ma trận xoay R bảo toàn chiều dài và góc: RᵀR=I, det(R)=+1. Tập các ma trận như vậy là SO(3). Ma trận đối xứng lệch [a]× cho phép viết a×b thành một phép nhân ma trận.</p><div class="formula">[a]× = [[0,−a₃,a₂],[a₃,0,−a₁],[−a₂,a₁,0]], &nbsp; a×b = [a]×b</div><p>Điều kiện det=+1 loại phép phản xạ gương, vốn cũng có RᵀR=I nhưng đảo tay hệ tọa độ.</p>')],
'cross','Cánh tay đòn r từ tâm tới motor và lực F tạo mô-men vuông góc mặt phẳng của chúng.',
'Chạy mã bên dưới; đổi a, b và thử một ma trận phản xạ có det = −1.',
['Nếu F song song r thì mô-men bằng bao nhiêu?','Vì sao RᵀR=I chưa đủ để khẳng định R∈SO(3)?'],'moment')

add(3,'Giải tích và phương trình vi phân','A1 · Toán công cụ',
'Đạo hàm nối trạng thái hiện tại với tốc độ thay đổi; tích phân số biến mô hình lực thành quỹ đạo theo thời gian.',
['Phân biệt gradient và Jacobian','Tuyến tính hóa quanh một điểm làm việc','So sánh Euler và RK4 khi giải ODE'],[
('Đạo hàm, gradient, Jacobian','<p>Vận tốc v=dr/dt, gia tốc a=dv/dt. Hàm nhiều biến có đạo hàm riêng: ∂f/∂x giữ các biến khác cố định. Gradient ∇f gom đạo hàm của một hàm vô hướng; Jacobian gom đạo hàm của hàm vector. Nếu ẋ=f(x,u), các Jacobian A=∂f/∂x và B=∂f/∂u cho mô hình gần đúng quanh trạng thái cân bằng.</p><div class="formula">f(x₀+δx,u₀+δu) ≈ f(x₀,u₀) + Aδx + Bδu</div><p>Đây là khai triển Taylor bậc một. Nó đúng khi δx, δu đủ nhỏ; không nên dùng xấp xỉ góc nhỏ cho động tác lật 90°.</p>'),
('ODE và ổn định','<p>Phương trình vi phân thường (ODE) mô tả quy luật thay đổi theo thời gian. Ví dụ ẋ=−kx với k&gt;0 có nghiệm x(t)=x₀e<sup>−kt</sup>, tiến về 0 nên ổn định tiệm cận. ẍ+ω₀²x=0 là dao động điều hòa không tắt; thêm cản c ẋ làm biên độ giảm.</p><p>Trong hệ quy chiếu quay, vector quan sát từ thế giới đổi ngay cả khi tọa độ body của nó cố định. Định lý vận chuyển:</p><div class="formula">(dv/dt)<sub>world</sub> = (dv/dt)<sub>body</sub> + ω × v</div><p>Ở đây các thành phần phải được biểu diễn cùng một hệ trục trước khi cộng.</p>'),
('Tích phân số','<p>Euler tiến dùng xₖ₊₁=xₖ+h f(xₖ,tₖ), dễ viết nhưng sai số toàn cục bậc O(h). RK4 lấy bốn độ dốc trong một bước, sai số toàn cục bậc O(h⁴) khi nghiệm đủ trơn. Bước h lớn có thể làm hệ ổn định trông như mất ổn định.</p><div class="formula">k₁=f(xₖ), k₂=f(xₖ+hk₁/2), k₃=f(xₖ+hk₂/2), k₄=f(xₖ+hk₃); xₖ₊₁=xₖ+h(k₁+2k₂+2k₃+k₄)/6</div>')],
'ode','Các bước tích phân xấp xỉ đường cong nghiệm liên tục; bước nhỏ thường giảm sai số.',
'Dùng con lắc góc nhỏ θ̈ + (g/L)θ = 0, θ(0)=0,2 rad, θ̇(0)=0. So θ(t) với 0,2 cos(√(g/L)t) cho h=0,1 và 0,01 s bằng Euler và RK4.',
['Jacobian có kích thước nào nếu f: R¹³×R⁴→R¹³?','Vì sao phải đưa các vector về cùng hệ trục khi dùng định lý vận chuyển?'])

add(4,'Hệ tọa độ và biểu diễn hướng','A1 · Toán công cụ',
'Một phép quay chỉ có nghĩa khi nói rõ nó biến vector từ hệ nào sang hệ nào và trục dương được chọn thế nào.',
['Dùng nhất quán ENU thế giới và FLU thân','Biết Euler ZYX, DCM, quaternion và axis-angle','Nhận ra gimbal lock và lỗi quy ước dấu'],[
('Quy ước cho toàn bộ khóa','<p><strong>World ENU:</strong> x hướng Đông, y hướng Bắc, z hướng lên. <strong>Body FLU:</strong> x hướng mũi drone, y sang trái, z lên trên. Cả hai thuận tay phải. R biến tọa độ body sang world: vʷ=Rvᵇ. Trọng lực trong world là (0,0,−mg); lực đẩy trong body là (0,0,T). NED/FRD cũng phổ biến, nhưng khi đổi quy ước phải đổi đồng thời dấu trong mọi công thức.</p>'),
('Euler và DCM','<p>Xoay chủ động quanh trục x, y, z lần lượt dùng Rx(φ), Ry(θ), Rz(ψ). Quy ước ZYX ở đây là R=Rz(ψ)Ry(θ)Rx(φ): với vector cột, Rx tác dụng trước. DCM (direction cosine matrix) chính là R; mỗi cột là một trục body viết trong world.</p><div class="formula">Rx(φ)=[[1,0,0],[0,cφ,−sφ],[0,sφ,cφ]]; Ry(θ)=[[cθ,0,sθ],[0,1,0],[−sθ,0,cθ]]; Rz(ψ)=[[cψ,−sψ,0],[sψ,cψ,0],[0,0,1]]</div><p>Khi pitch θ=±90°, hai trục Euler trùng nhau và không còn tách riêng roll/yaw: đó là gimbal lock. Vật thể vẫn quay bình thường; chỉ cách ghi ba góc bị suy biến.</p>'),
('Quaternion và các lựa chọn','<p>Quaternion đơn vị q=(w,x,y,z) biểu diễn quay góc α quanh trục đơn vị u bằng q=(cos(α/2),u sin(α/2)). Tích Hamilton ghép hai phép quay; nếu q=(w,v), p=(s,u) thì q⊗p=(ws−v·u, wu+sv+v×u). Quaternion nghịch đảo q⁻¹=(w,−x,−y,−z) khi |q|=1. Xoay vector v bằng phần vector của q⊗(0,v)⊗q⁻¹. q và −q biểu diễn cùng một hướng.</p><p>Chuyển Euler ZYX sang quaternion bằng q=qz(ψ)⊗qy(θ)⊗qx(φ). Đổi q sang DCM bằng các cột thu được khi xoay e₁,e₂,e₃ bằng q; đổi DCM sang Euler bằng θ=asin(−R₃₁), φ=atan2(R₃₂,R₃₃), ψ=atan2(R₂₁,R₁₁) khi cosθ≠0. Chuyển DCM sang quaternion cần chọn nhánh ổn định số, thường qua trace hoặc phần tử đường chéo lớn nhất.</p><p>Euler dễ đọc nhưng có điểm kỳ dị; DCM dễ biến đổi vector nhưng cần 9 số và tái trực giao hóa; quaternion cần 4 số, không có gimbal lock khi tích phân, nhưng cần chuẩn hóa; axis-angle trực quan cho một phép quay, kém tiện khi ghép liên tục.</p>')],
'frames','Trục thân FLU quay cùng drone; trục thế giới ENU đứng yên.',
'Trong Python dùng scipy.spatial.transform.Rotation. Kiểm tra RᵀR≈I, det R≈1 và round-trip Euler→q→R→Euler ở các góc tránh pitch ±90°. Trong C, dùng quaternion đơn vị và tolerance cho so sánh số thực.',
['R biến tọa độ từ body sang world hay ngược lại?','Quaternion q và −q biểu diễn hướng khác nhau không?'])

add(5,'Động học (kinematics)','A1 · Toán công cụ',
'Động học mô tả vị trí và hướng thay đổi thế nào từ vận tốc, chưa cần biết lực đã sinh ra các vận tốc đó.',
['Viết ṙ và Ṙ từ vận tốc','Liên hệ tốc độ góc body với tốc độ Euler','Tích phân quaternion mà vẫn giữ chuẩn 1'],[
('Vị trí và vận tốc trong hai hệ','<p>Gọi rʷ là vị trí tâm khối lượng trong world, vᵇ là vận tốc biểu diễn trong body. Khi đó ṙʷ=Rvᵇ. Nếu lưu vʷ trực tiếp, ṙʷ=vʷ. Không cộng các thành phần body vào tọa độ world khi drone đang quay.</p>'),
('Tốc độ góc không phải đạo hàm Euler','<p>Gyro đo ωᵇ=(p,q,r), trong đó p,q,r là tốc độ quay quanh trục body tức thời. Với Euler ZYX:</p><div class="formula">[p,q,r]ᵀ = W(φ,θ)[φ̇,θ̇,ψ̇]ᵀ, &nbsp; W=[[1,0,−sinθ],[0,cosφ,sinφ cosθ],[0,−sinφ,cosφ cosθ]]</div><p>Khi θ gần ±90°, W khó nghịch đảo. Ở góc nhỏ, p≈φ̇, q≈θ̇, r≈ψ̇; ngoài vùng đó không thể thay trực tiếp.</p>'),
('Tích phân tư thế','<p>Với R biến body→world và ω biểu diễn trong body, Ṙ=R[ω]×. Với quaternion q cùng quy ước, q̇=½q⊗(0,ω). Sau mỗi bước số, chuẩn hóa q←q/|q| để hạn chế trôi chuẩn do sai số làm tròn.</p><div class="formula">qₖ₊₁ ≈ normalize(qₖ + (Δt/2) qₖ⊗(0,ωₖ))</div><p>Chuẩn hóa sửa ràng buộc hình học, không sửa lỗi mô hình gyro. Với bước lớn hoặc quay nhanh, dùng phép quay gia số exp(½Δtω) cho độ chính xác tốt hơn.</p>')],
'rotation','Vector vận tốc góc nằm theo trục quay; các trục body chuyển động theo vật thể.',
'Khởi tạo q=(1,0,0,0), ωᵇ=(0,0,π/2) rad/s, Δt=0,01 s. Tích phân 1 s, vẽ trục thân trong 3D và kiểm tra yaw gần 90°, |q|≈1.',
['Vì sao p,q,r không luôn bằng φ̇,θ̇,ψ̇?','Điều gì xảy ra nếu không chuẩn hóa q sau nhiều bước?'])

exec((ROOT/'more_lessons.py').read_text(encoding='utf-8'))
exec((ROOT/'matrix_lessons.py').read_text(encoding='utf-8'))

def diagram(kind):
    head='''<svg viewBox="0 0 700 310" role="img" aria-label="Sơ đồ minh họa bài học"><defs><marker id="arrow-teal" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#08a69b"/></marker><marker id="arrow-orange" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#da7941"/></marker></defs>'''
    drone='''<g stroke="#6689a6" stroke-width="12" stroke-linecap="round"><path d="M350 155L230 60M350 155L470 60M350 155L470 250M350 155L230 250"/></g><circle cx="350" cy="155" r="28" class="drone-body"/><text x="350" y="162" text-anchor="middle" fill="white">CG</text>'''
    motors=''.join(f'<g><circle class="rotor" cx="{x}" cy="{y}" r="27"/><g class="spin" style="transform-origin:{x}px {y}px;animation-direction:{"reverse" if i in (1,3) else "normal"}"><ellipse cx="{x}" cy="{y}" rx="24" ry="5" fill="#75b4d4" opacity=".8"/><ellipse cx="{x}" cy="{y}" rx="5" ry="24" fill="#75b4d4" opacity=".8"/></g><circle cx="{x}" cy="{y}" r="6" fill="#204b72"/><text x="{x}" y="{y+43}" text-anchor="middle" font-weight="bold" fill="#204b72">M{i}</text></g>' for i,(x,y) in enumerate([(230,60),(470,60),(470,250),(230,250)],1))
    axis='''<path d="M125 240V150" class="axis-x" stroke-width="3" marker-end="url(#arrow-orange)"/><path d="M125 240H35" class="axis-y" stroke-width="3" marker-end="url(#arrow-teal)"/><text x="115" y="138">x / mũi</text><text x="35" y="263">y / trái</text>'''
    if kind in ('drone','mixer'):
        body=drone+motors+axis+('<text x="350" y="20" text-anchor="middle">M1, M3: CCW ↺ · M2, M4: CW ↻</text>' if kind=='mixer' else '<text x="350" y="25" text-anchor="middle" font-weight="bold">MŨI DRONE ↑</text>')
    elif kind in ('forces','air','disk'):
        body='''<ellipse cx="350" cy="145" rx="130" ry="15" fill="#d9edf9" stroke="#28719f" stroke-width="3"/><rect x="323" y="130" width="54" height="35" rx="7" class="drone-body"/><path d="M350 115V35" class="svg-thrust"/><text x="368" y="65" fill="#008e88">T</text><path d="M350 170V250" class="svg-gravity"/><text x="365" y="235" fill="#d47a2c">mg</text>'''
        if kind in ('air','disk'): body+='''<path d="M250 170Q220 215 270 285M450 170Q480 215 430 285M300 170V280M400 170V280" stroke="#81b9d6" stroke-width="3" fill="none" marker-end="url(#arrow-teal)"/><text x="485" y="225">dòng khí xuống</text>'''
        if kind=='disk': body+='''<text x="145" y="65">v∞ = 0</text><text x="145" y="150">tại đĩa: vᵢ</text><text x="145" y="270">xa dưới: 2vᵢ</text>'''
    elif kind in ('cross','inertia'):
        body='''<circle cx="220" cy="205" r="18" fill="#204b72"/><text x="190" y="240">CG</text><path d="M220 205H470" stroke="#6689a6" stroke-width="12"/><circle cx="470" cy="205" r="24" class="rotor"/><path d="M470 190V65" class="svg-thrust"/><text x="485" y="90" fill="#008e88">F</text><text x="335" y="225">r</text><path d="M300 130C340 85 410 100 420 125" class="svg-gravity"/><text x="340" y="80">τ = r × F</text>'''
        if kind=='inertia':body+='<circle cx="540" cy="205" r="15" fill="#da7941"/><text x="520" y="250">pin xa tâm → J lớn</text>'
    elif kind in ('frames','rotation'):
        body='''<circle cx="355" cy="180" r="20" class="drone-body"/><path d="M355 180L475 130" class="axis-x" stroke-width="5" marker-end="url(#arrow-orange)"/><path d="M355 180L270 105" class="axis-y" stroke-width="5" marker-end="url(#arrow-teal)"/><path d="M355 180V65" class="axis-z" stroke-width="5"/><text x="480" y="125">xᵇ</text><text x="245" y="95">yᵇ</text><text x="365" y="60">zᵇ</text><path d="M85 240H190M85 240V135" stroke="#9db4c8" stroke-width="3"/><text x="195" y="245">E</text><text x="70" y="125">N</text><text x="80" y="275">World ENU</text><text x="335" y="245">Body FLU</text>'''
        if kind=='rotation':body+='<path d="M405 210A90 90 0 0 0 450 165" fill="none" stroke="#d47a2c" stroke-width="4"/><text x="470" y="205">ωᵇ</text>'
    elif kind=='ode':
        pts=[(70,220),(120,185),(170,157),(220,140),(270,142),(320,157),(370,184),(420,212),(470,229),(520,225),(570,205),(620,175)]
        poly=' '.join(f'{x},{y}' for x,y in pts)
        body=f'<path d="M55 250H650M65 45V250" stroke="#9db4c8" stroke-width="2"/><path d="M70 220C180 90 250 110 360 180S520 265 630 160" fill="none" stroke="#08a69b" stroke-width="4"/><polyline points="{poly}" fill="none" stroke="#d47a2c" stroke-width="3"/>'+''.join(f'<circle cx="{x}" cy="{y}" r="4" fill="#d47a2c"/>' for x,y in pts)+'<text x="500" y="65">nghiệm liên tục</text><text x="500" y="88" fill="#d47a2c">bước số</text>'
    elif kind in ('flow','motor','sim'):
        boxes={'flow':['Ω motor','T, Q','F, τ','r̈, ω̇','r, q'],'motor':['Pin','ESC','dòng i','Ω rotor','T, Q'],'sim':['Lệnh','Motor','Newton–Euler','RK4','Trạng thái']}[kind]
        body=''.join(f'<g><rect x="{35+i*135}" y="105" width="112" height="82" rx="14" fill="{["#d9edf9","#e2f4ef","#f9ead8","#d9edf9","#e2f4ef"][i]}" stroke="#7ca5c3"/><text x="{91+i*135}" y="151" text-anchor="middle" font-weight="bold" font-size="15">{escape(b)}</text></g>' for i,b in enumerate(boxes))
        body+=''.join(f'<path d="M{148+i*135} 146H{166+i*135}" class="svg-thrust"/>' for i in range(4))
        if kind=='sim':body+='<path d="M635 200V260H90V202" fill="none" stroke="#d47a2c" stroke-width="3" marker-end="url(#arrow-orange)"/><text x="320" y="288">kiểm tra và vẽ đồ thị</text>'
    elif kind=='effects':
        body='''<circle cx="350" cy="150" r="48" fill="#204b72"/><text x="350" y="156" text-anchor="middle" fill="white">Drone</text><circle cx="350" cy="150" r="100" fill="none" stroke="#08a69b" stroke-width="3"/><circle cx="350" cy="150" r="145" fill="none" stroke="#d47a2c" stroke-width="3"/><text x="465" y="80">lực chính</text><text x="505" y="250">bậc hai + môi trường</text>'''
    else:
        body='''<path d="M70 240H640M70 240V40" stroke="#9db4c8" stroke-width="2"/><path d="M90 225Q240 180 350 120T625 55" fill="none" stroke="#08a69b" stroke-width="4"/><path d="M220 190L460 110" stroke="#d47a2c" stroke-width="4"/><circle cx="340" cy="150" r="7" fill="#204b72"/><text x="430" y="95">phi tuyến</text><text x="465" y="150">tiếp tuyến hover</text>'''
    return head+body+'</svg>'

groups=[('A1 · Toán công cụ',1,5),('A2 · Cơ học',6,7),('A3 · Khí động học và động cơ',8,12),('A4 · Tổng hợp thành mô hình',13,15)]
def nav(current=None):
    out='<a class="brand" href="index.html">✦ Drone từ gốc</a><nav aria-label="Danh sách bài học">'
    for name,start,end in groups:
        out+=f'<small>{escape(name)}</small><ol>'
        for n in range(start,end+1):
            l=LESSONS[n-1]; active=' class="active" aria-current="page"' if current==n else ''
            out+=f'<li><a{active} href="A{n:02}.html">A{n}. {escape(l["title"])}</a></li>'
        out+='</ol>'
    out+='<small>B · Điều khiển PID</small><ol>'
    for n,title in enumerate(('Cần bao nhiêu vòng PID?', 'PID rời rạc và cách chỉnh định', 'Triển khai Python/C và mô phỏng'),1):
        active=' class="active" aria-current="page"' if current==f'B{n}' else ''
        out+=f'<li><a{active} href="B{n:02}.html">B{n}. {escape(title)}</a></li>'
    out+='</ol><small>C · Cảm biến và flight controller</small><ol>'
    for n,title in enumerate(('Cảm biến và hiệu chuẩn','Ước lượng tư thế và sensor fusion','Đóng vòng điều khiển thật','Tích hợp, kiểm thử và an toàn'),1):
        active=' class="active" aria-current="page"' if current==f'C{n}' else ''
        out+=f'<li><a{active} href="C{n:02}.html">C{n}. {escape(title)}</a></li>'
    out+='</ol>'
    return out+'</nav>'

def frame(title,inner,current=None,demo=''):
    extra='<link rel="stylesheet" href="assets/6dof.css">' if current==1 else ('<link rel="stylesheet" href="assets/matrix-viz.css">' if current in (2,4,10) else ('<link rel="stylesheet" href="assets/c-course.css">' if isinstance(current,str) and current.startswith('C') else ''))
    script='<script src="assets/6dof.js" defer></script>' if current==1 else ('<script src="assets/matrix-viz.js" defer></script>' if current in (2,4,10) else ('<script src="assets/c-course.js" defer></script>' if isinstance(current,str) and current.startswith('C') else ''))
    return f'''<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><title>{escape(title)} · Drone từ gốc</title><link rel="stylesheet" href="assets/style.css"><link rel="stylesheet" href="assets/pid.css">{extra}</head><body data-demo="{demo}"><div class="layout"><aside class="side">{nav(current)}</aside><main class="main">{inner}</main></div><script src="assets/app.js" defer></script>{script}</body></html>'''

def lesson_page(l):
    n=l['num']; title=l['title']
    goals=''.join(f'<li>{escape(x)}</li>' for x in l['goals'])
    sections=''
    for i,(h,body) in enumerate(l['sections']):
        sections+=f'<section class="card"><h2>{escape(h)}</h2>{body}{MATRIX_NOTES.get((n,i),"")}</section>'
        sections+=MATRIX_DEMOS.get((n,i),'')
        if n==1 and i==0:
            sections+='''<section class="lab six-dof" id="six-dof"><h2>Khám phá 6 bậc tự do trong 3D</h2><p>Di chuyển từng thanh để thấy drone tịnh tiến theo x, y, z hoặc quay quanh trục thân: roll φ, pitch θ, yaw ψ. Kéo trên hình để đổi góc nhìn.</p><div class="six-dof-layout"><div class="six-dof-scene"><canvas id="six-dof-canvas" aria-label="Mô hình drone 3D với các trục tọa độ, thay đổi theo sáu thanh điều chỉnh"></canvas><div class="six-dof-legend"><span><i class="axis-dot axis-dot-x"></i>x thế giới: Đông</span><span><i class="axis-dot axis-dot-y"></i>y thế giới: Bắc</span><span><i class="axis-dot axis-dot-z"></i>z: lên</span></div></div><div class="six-dof-panel"><div class="six-dof-controls" id="six-dof-controls"></div><button type="button" id="six-dof-reset">Đặt lại trạng thái</button><p class="six-dof-readout" id="six-dof-readout" aria-live="polite"></p></div></div><p class="caption">Các thanh đặt trực tiếp tư thế và vị trí để học hình học 6-DOF; đây không phải mô phỏng động lực học hay lệnh motor. Góc dương theo quy tắc bàn tay phải, phép quay R = Rz(ψ) Ry(θ) Rx(φ).</p></section>'''
    checks=''.join(f'<li>{escape(x)}</li>' for x in l['checks'])
    prev=f'<a href="A{n-1:02}.html">← A{n-1}</a>' if n>1 else '<a href="index.html">← Mục lục</a>'
    nxt=f'<a href="A{n+1:02}.html">A{n+1} →</a>' if n<15 else '<a href="B01.html">B1 · PID →</a>'
    demo=f'<section class="lab"><h2>Thử thay số</h2><div data-demo></div></section>' if l['demo'] else ''
    special=''
    if n==1:special='''<section class="card"><h2>Sơ đồ phụ thuộc của Phần A</h2><div class="table-wrap"><table><tr><th>Nền tảng</th><th>Dùng để hiểu</th><th>Dẫn tới</th></tr><tr><td>A2 vector, ma trận; A3 đạo hàm, ODE</td><td>A4 hệ trục, phép quay; A5 động học</td><td>A13 trạng thái và phương trình</td></tr><tr><td>A6 Newton; A7 vật rắn</td><td>A8–A9 không khí và cánh quạt; A10–A12 motor, mixer, pin</td><td>A13 lực và mô-men thực tế</td></tr><tr><td>A13 Newton–Euler</td><td>A14 tuyến tính hóa</td><td>A15 mô phỏng và kiểm chứng</td></tr></table></div></section>'''
    if n==2:special='''<section class="lab"><h2>NumPy: kiểm chứng phép nhân</h2><pre>import numpy as np
a = np.array([1., 2., 3.]); b = np.array([4., -1., 2.])
ax = np.array([[0,-a[2],a[1]],[a[2],0,-a[0]],[-a[1],a[0],0]])
assert np.allclose(np.cross(a,b), ax @ b)
R = np.array([[0,-1,0],[1,0,0],[0,0,1]])
assert np.allclose(R.T @ R, np.eye(3))
assert np.isclose(np.linalg.det(R), 1)</pre></section>'''
    if n==3:special='''<section class="lab"><h2>Python: Euler và RK4 cho con lắc góc nhỏ</h2><pre>import numpy as np
g, L = 9.81, 1.0
def f(y): return np.array([y[1], -(g/L)*y[0]])
def euler(y,h): return y + h*f(y)
def rk4(y,h):
    k1=f(y); k2=f(y+h*k1/2)
    k3=f(y+h*k2/2); k4=f(y+h*k3)
    return y+h*(k1+2*k2+2*k3+k4)/6
for h in (0.1,0.01):
    for step in (euler,rk4):
        y=np.array([0.2,0.0])
        for _ in range(round(10/h)): y=step(y,h)
        exact=0.2*np.cos(np.sqrt(g/L)*10)
        print(h,step.__name__,abs(y[0]-exact))</pre></section>'''
    if n==4:special='''<section class="lab"><h2>Kiểm thử phép quay</h2><pre>from scipy.spatial.transform import Rotation as Rot
import numpy as np
r = Rot.from_euler('ZYX', [30, 20, 10], degrees=True)
R, q_xyzw = r.as_matrix(), r.as_quat()
assert np.allclose(R.T @ R, np.eye(3), atol=1e-12)
assert np.allclose(Rot.from_quat(q_xyzw).as_matrix(), R)
# SciPy lưu quaternion theo [x,y,z,w]; bài học dùng [w,x,y,z].</pre><p>Trong C, viết các hàm <code>quat_mul</code>, <code>quat_normalize</code>, <code>quat_to_dcm</code>; unit test identity, quay 90° quanh từng trục và round-trip với tolerance 1e−6.</p></section>'''
    if n==5:special='''<section class="lab"><h2>Python: hiển thị trục body trong 3D</h2><pre>import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation as Rot
dt, omega = 0.01, np.array([0, 0, np.pi/2])
rot = Rot.identity()
for _ in range(100):
    rot = rot * Rot.from_rotvec(omega*dt)
R = rot.as_matrix()
fig = plt.figure(); ax = fig.add_subplot(projection='3d')
for i, color in enumerate(('r','g','b')):
    ax.quiver(0,0,0,*R[:,i],color=color,length=1)
ax.set(xlim=(-1,1),ylim=(-1,1),zlim=(-1,1))
plt.show()</pre><p>Trục đỏ/x, xanh lá/y, xanh dương/z cho thấy vật thể quay 90° quanh z sau 1 giây. <code>Rot</code> dùng quaternion nội bộ; mã trên áp dụng ω trong body.</p></section>'''
    if n==10:special='''<section class="lab"><h2>Python: kiểm tra mixer X</h2><pre>import numpy as np
a, kT, kQ = 0.18, 1.5e-5, 3e-7
M = np.array([[kT,kT,kT,kT],
              [a*kT,-a*kT,-a*kT,a*kT],
              [-a*kT,-a*kT,a*kT,a*kT],
              [-kQ,kQ,-kQ,kQ]])
u = np.array([9.81, 0.02, 0.0, 0.0])
s = np.linalg.solve(M,u) # s_i = Ω_i²
assert np.all(s >= 0)
assert np.allclose(M @ s, u)
print(np.sqrt(s)) # rad/s</pre></section>'''
    if n==13:special='''<section class="lab"><h2>Khung hàm f(x, Ω)</h2><pre>import numpy as np
def f(x, Omega, m, J, kT, kQ, a):
    pos, vel, quat, rate = x[:3], x[3:6], x[6:10], x[10:13]
    thrust = kT * Omega**2
    T = thrust.sum()
    tau = np.array([a*(thrust[0]-thrust[1]-thrust[2]+thrust[3]),
                    a*(-thrust[0]-thrust[1]+thrust[2]+thrust[3]),
                    (kQ/kT)*(-thrust[0]+thrust[1]-thrust[2]+thrust[3])])
    # Cần tự viết quat_to_R và quat_mul, với q=[w,x,y,z].
    R = quat_to_R(quat)
    qdot = 0.5 * quat_mul(quat, np.r_[0.0, rate])
    acc = -np.array([0,0,9.81]) + (T/m)*R[:,2]
    rate_dot = np.linalg.solve(J, tau - np.cross(rate,J@rate))
    return np.r_[vel, acc, qdot, rate_dot]</pre><p>Khung này bỏ lực cản và gyro rotor. Kiểm tra kích thước vector, chuẩn quaternion và đơn vị trước khi thêm hiệu ứng khác.</p></section>'''
    if n==15:special='''<section class="lab"><h2>Vòng lặp mô phỏng tối thiểu</h2><pre>for k in range(num_steps):
    desired = controller_or_test_signal(t, state)
    omega_cmd = allocate_and_clip(desired, M, omega_max)
    # Tích phân chung cả trạng thái drone và bốn Ω motor.
    state = rk4(full_dynamics, state, omega_cmd, dt)
    state[6:10] /= np.linalg.norm(state[6:10])
    log.append(state.copy())
    t += dt</pre><p>Để chạy được, triển khai các hàm từ A10 và A13, rồi thêm trạng thái motor Ω̇=(Ωcmd−Ω)/τm. Đầu ra của kiểm chứng là đồ thị, không chỉ thông báo “chạy thành công”.</p></section>'''
    inner=f'''<header class="hero"><span class="eyebrow">{escape(l['group'])} · Bài A{n}</span><h1>{escape(title)}</h1><p class="lead">{escape(l['lead'])}</p><div class="meta"><span class="pill">Người mới bắt đầu</span><span class="pill">Lý thuyết + minh họa + thực hành</span></div></header><section class="card"><h2>Sau bài này, bạn sẽ</h2><ul>{goals}</ul></section><figure class="figure">{diagram(l['diagram'])}<figcaption class="caption">{escape(l['caption'])}</figcaption></figure>{sections}{demo}{special}<section class="exercise"><h2>Thực hành</h2><p>{escape(l['practice'])}</p><details><summary>Câu hỏi tự kiểm tra</summary><ol>{checks}</ol></details></section><nav class="navfoot" aria-label="Chuyển bài">{prev}{nxt}</nav>'''
    return frame(f'A{n}. {title}',inner,n,l['demo'])

index_intro='''<header class="hero"><span class="eyebrow">Khóa học · Phần A–C</span><h1>Từ cơ học bay tới flight controller</h1><p class="lead">22 bài học tiếng Việt: 15 bài nền tảng, 3 bài PID và 4 bài về cảm biến, ước lượng trạng thái, vòng kín và triển khai thực tế. Mỗi bài có giải thích, ứng dụng, sơ đồ hoặc mô phỏng và bài thực hành.</p><div class="meta"><span class="pill">Đọc offline</span><span class="pill">Mô phỏng tương tác</span><span class="pill">Quy ước ENU / FLU</span></div></header><section class="card"><h2>Cách học</h2><p>Đọc theo thứ tự nếu bạn mới bắt đầu. Nếu đã vững đại số và giải tích, có thể đọc nhanh A2–A3 và tập trung A9, A10, A13 trước khi sang B1–B3, rồi học C1–C4 để nối cảm biến với điều khiển. Trong toàn bộ khóa: world ENU có z hướng lên; body FLU có x hướng mũi, y sang trái, z lên; R đổi vector body sang world.</p><p>Thông số số học trong ví dụ là minh họa. Khi chọn phần cứng, hãy thay bằng dữ liệu đo của motor, cánh quạt, pin và khối lượng thực tế.</p></section>'''
exec((ROOT/'pid_lessons.py').read_text(encoding='utf-8'))
exec((ROOT/'c_lessons.py').read_text(encoding='utf-8'))
cards='<section class="roadmap">'+''.join(f'<a href="A{l["num"]:02}.html"><span>{escape(l["group"])} · A{l["num"]}</span><strong>{escape(l["title"])}</strong><span>{escape(l["lead"])}</span></a>' for l in LESSONS)+''.join(f'<a href="B{l["num"]:02}.html"><span>B · Điều khiển PID · B{l["num"]}</span><strong>{escape(l["title"])}</strong><span>{escape(l["lead"])}</span></a>' for l in PID_LESSONS)+''.join(f'<a href="C{l["num"]:02}.html"><span>C · Cảm biến và flight controller · C{l["num"]}</span><strong>{escape(l["title"])}</strong><span>{escape(l["lead"])}</span></a>' for l in C_LESSONS)+'</section>'
if __name__=='__main__':
    assert len(LESSONS)==15 and [x['num'] for x in LESSONS]==list(range(1,16))
    (ROOT/'index.html').write_text(frame('Mục lục',index_intro+cards),encoding='utf-8')
    for l in LESSONS:(ROOT/f'A{l["num"]:02}.html').write_text(lesson_page(l),encoding='utf-8')
    for l in PID_LESSONS:(ROOT/f'B{l["num"]:02}.html').write_text(pid_page(l),encoding='utf-8')
    for l in C_LESSONS:(ROOT/f'C{l["num"]:02}.html').write_text(c_page(l),encoding='utf-8')
    print('Built',len(LESSONS)+len(PID_LESSONS)+len(C_LESSONS),'lessons')
