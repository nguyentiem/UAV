# Hướng dẫn cho các bài giảng trong project 

Áp dụng cho mọi bài giảng HTML tạo hoặc sửa trong thư mục này, kể cả ở các phiên trò chuyện sau.

1. Đọc prompt chung và prompt riêng của bài trong `drone-lesson-prompts.md` trước khi tạo bài. Mỗi bài là một file HTML độc lập, mở trực tiếp bằng trình duyệt.
2. Với công thức toán học, dùng KaTeX từ `cdnjs.cloudflare.com` và **kiểm tra URL CSS lẫn JavaScript trả HTTP 200** trước khi ghi phiên bản vào HTML. KaTeX `0.16.22` trên cdnjs trả 404; phiên bản `0.18.0` đã được kiểm tra hoạt động ngày 2026-10-12. Không chép lại URL chưa xác minh từ bài cũ.
3. Sau khi tạo hoặc sửa bài, mở file bằng `file://` trong trình duyệt thật. Kiểm tra KaTeX đã tải, số công thức được dựng bằng số phần tử nguồn (`[data-math]` hoặc `[data-katex]`), không có `.katex-error`, và không có lỗi JavaScript trong console. Kiểm tra trực quan ít nhất một công thức dài hoặc ma trận.
4. Nếu dùng thuộc tính HTML để chứa LaTeX, bảo đảm ký tự đặc biệt như `&` được escape đúng; không để người học thấy mã LaTeX thô do CDN lỗi. Có nội dung dự phòng dễ đọc nếu KaTeX không tải được.
5. Kiểm tra các slider, nút, animation, dữ liệu tính toán, bài trắc nghiệm và bố cục di động. Dữ liệu trên hình, công thức và code Python phải nhất quán. Với hình không gian, dùng phép chiếu 3D có trục và nhãn rõ, cho phép đổi góc nhìn khi chủ đề cần.
6. Khi cập nhật một lỗi chung, sửa cả các bài HTML hiện có bị ảnh hưởng và cập nhật prompt chung để các bài sau không lặp lỗi.
7. cung cấp một HMTL link tới các bài học , mỗi bài học sẽ có nút next bài và pre bài tiện lợi có thể bấm bất cứ lúc nào 

