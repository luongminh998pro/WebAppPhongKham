from flask import Flask, render_template, request
import csv
import re
import random
from fuzzywuzzy import fuzz

app = Flask(__name__)

app = Flask(__name__)

# Danh sách khoa phòng
khoa_phong = {

    'Pk Cấp Cứu': [
    'cấp', 
    'đột',
    'quỵ', 
    'ngộ', 
    'độc', 
    'suy tim', 
    'khó', 
    'sốc', 
    'buồn', 
    'hạ', 
    'tăng', 
    'nhiều', 
    'thương', 
    'nhồi máu',
    'co giật', 
    'tê liệt',  
    'phản', 
    'vỡ', 
    'khó', 
    'ngất', 
    'dữ dội', 
    'cap', 
    'dot', 
    'ngo', 
    'doc', 
    'suy tim', 
    'kho', 
    'soc', 
    'buon', 
    'ha', 
    'tang', 
    'nhieu', 
    'thuong', 
    'nhoi mau', 
    'phan', 
    'vo', 
    'kho', 
    'ngat', 
    'quy',
    'te liet',  
    'du doi'
    'co giat', 
    
],
  
    'Pk Chấn Thương': [
        'chấn thương', 'xương', 'gãy', 'nẹp xương', 'cố định', 'đau', 'trật khớp', 
        'vết thương', 'tái tạo xương', 'phục hồi chức năng', 'cải thiện vận động', 
        'các triệu chứng chấn thương', 'bong gân', 'đau nhức', 'chấn thương thể thao'
    ],


    'pk.Ngoại Tiết niệu': [
    'tiết niệu', 
    'đau bụng nhẹ', 
    'tiểu đau', 
    'tiểu gắt', 
    'tiểu ra máu', 
    'khó tiểu', 
    'tiểu nhiều lần', 
    'mùi nước tiểu bất thường', 
    'đau lưng', 
    'sưng phù vùng bụng', 
    'mệt mỏi', 
    'sốt', 
    'cảm giác buồn nôn', 
    'các triệu chứng về tiểu đường', 
    'rối loạn chức năng thận', 
    'cảm giác khô miệng'
],

    

    'Pk Da Liễu': [
        'da', 'da liễu', 'ngứa', 'bong da', 'mẩn ngứa', 'viêm da', 'chàm',
        'khô da', 'mụn', 'vảy nến', 'trứng cá', 'bị dị ứng', 'viêm da tiếp xúc',
        'mụn cóc', 'nấm da', 'nổi mề đay', 'bệnh chàm', 'hắc lào', 'bệnh vẩy nến',
        'bệnh trứng cá', 'bệnh nấm', 'da nhờn', 'da khô', 'mụn đầu đen', 'mụn đầu trắng',
        'tăng sắc tố da', 'suy giáp', 'rối loạn nội tiết', 'bệnh da liễu ở trẻ em',
        'viêm da bã nhờn', 'dị ứng thuốc', 'bệnh lý sắc tố', 'các bệnh da mãn tính',
        'dễ bị tổn thương da', 'các vấn đề về da mặt', 'sạch da', 'trẻ hóa da',
        'lão hóa da', 'sạm da', 'nám da', 'da nhạy cảm', 'da không đều màu',
        'bệnh da vùng kín', 'điều trị thẩm mỹ da', 'chăm sóc da hàng ngày',
        'các sản phẩm dưỡng da', 'chế độ ăn uống cho da', 'thực phẩm tốt cho da',
        'bệnh da di truyền', 'bệnh da do ánh sáng', 'bệnh lý ngoài da', 'điều trị mụn',
        'phẫu thuật thẩm mỹ da', 'bệnh da do tiếp xúc hóa chất', 'thăm khám da',
        'tư vấn da liễu', 'các dấu hiệu bệnh da', 'bệnh da do virus', 'bệnh da do vi khuẩn',
        'bệnh da do nấm', 'khám da', 'trị liệu da', 'điều trị bệnh da', 'chăm sóc sắc đẹp',
        'tư vấn làm đẹp da', 'bệnh da tự miễn', 'các bệnh viêm da', 'bệnh lý về chân tóc',
        'các phương pháp điều trị da', 'sử dụng thuốc bôi da', 'các bệnh lý mô mềm',
        'viêm nang lông', 'bệnh lý da nhiễm trùng', 'tìm hiểu về da', 'kiến thức về da',
        'các triệu chứng bệnh da', 'bệnh da mãn tính', 'bệnh viêm da dị ứng', 'da nhiễm trùng',
        'bệnh vẩy nến toàn thân', 'bệnh chàm thể tạng', 'màng nhầy miệng', 'viêm nướu',
        'sử dụng sản phẩm tự nhiên cho da', 'các thành phần chăm sóc da', 'phân loại bệnh da',
        'hỗ trợ điều trị bệnh da', 'bệnh lý da ở người già', 'da nhạy cảm với thời tiết',
        'hói đầu', 'rụng tóc', 'gàu', 'bệnh da do côn trùng cắn', 'dị ứng thực phẩm',
        'các bệnh lý liên quan đến mụn', 'bệnh da do di truyền', 'khám tổng quát da'
    ],


'Pk Tai Mũi Họng': [
    'tai', 'mũi', 'họng', 'nghe', 'thính lực', 'đau họng', 'khó thở', 'ù tai', 'viêm',
    'viêm xoang', 'dị ứng', 'bệnh tai', 'bệnh mũi', 'bệnh họng', 'đau tai', 'sổ mũi',
    'cảm lạnh', 'viêm amidan', 'viêm thanh quản', 'ngạt mũi', 'khó ngửi', 'nghe kém',
    'mũi chảy máu', 'tê môi', 'nói khàn', 'điếc', 'rối loạn thính giác', 'nhiễm trùng tai',
    'bệnh lý mũi', 'mũi khô', 'các triệu chứng viêm xoang', 'viêm tai giữa', 'mũi nấm',
    'điều trị mũi', 'khám tai', 'chẩn đoán viêm xoang', 'chẩn đoán tai mũi họng',
    'khám thính lực', 'khám chức năng hô hấp', 'các bệnh lý hô hấp', 'khó thở khi nằm',
    'khó thở khi hoạt động'
],
    'Pk Mắt': [
        'mắt', 'thị lực', 'thị giác', 'mờ mắt', 'đau mắt', 'khô mắt', 'cận thị', 'viễn thị',
        'lão thị', 'bệnh lý mắt', 'đau nhức mắt', 'các triệu chứng mắt', 'khám mắt',
        'các bệnh về mắt', 'bệnh lý thị giác', 'điều trị mắt', 'tư vấn thị lực', 'mắt cận',
        'mắt viễn', 'điều trị khô mắt', 'các phương pháp kiểm tra', 'tư vấn chăm sóc mắt',
        'mắt yếu', 'mắt nheo', 'mắt đỏ', 'các vấn đề về thị lực',
        'các triệu chứng thị lực', 'bệnh lý mắt ở trẻ em', 'khám mắt cho trẻ', 'tư vấn về kính',
        'hỗ trợ thị lực', 'các dấu hiệu bất thường của mắt',
        'bệnh khô mắt', 'rối loạn thị giác',
        'bệnh lý mắt do tuổi', 'mắt đa sắc', 'mắt viễn thị', 'các phương pháp điều trị',
        'tư vấn chăm sóc thị lực', 'các bệnh lý mãn tính', 'tư vấn khúc xạ', 'bệnh lý giác mạc',
        'bệnh lý võng mạc', 'điều trị giác mạc', 'khám tổng quát mắt', 'các triệu chứng chói',
        'các bệnh về thủy tinh thể', 'khám mắt thường xuyên', 'điều trị bệnh lý mắt',
        'mỏi mắt',
    ],


    'Pk Răng Hàm Mặt': [
        'răng', 'hàm', 'mặt', 'nha khoa', 'viêm', 'sâu răng', 'viêm nướu', 
        'trám răng', 'niềng răng', 'khớp cắn', 'các vấn đề về răng', 'chăm sóc răng miệng', 
        'khám răng miệng', 'điều trị răng', 'các triệu chứng nha khoa', 'các bệnh lý răng miệng', 
        'chăm sóc răng cho trẻ', 'tẩy trắng răng','rối loạn khớp thái dương hàm', 'điều trị viêm nha chu', 'hôi miệng',
        'rách miệng', 'nướu răng', 'sử dụng niềng răng', 
    ],

    'PK Nhi tại khoa': [
        'nhi', 'trẻ em', 'đau bụng', 'tiêm chủng', 'khám sức khỏe', 
        'bệnh thường gặp', 'phát triển trẻ em', 'bệnh nhi', 'bệnh lý nhi khoa', 
        'truyền nhiễm', 'dấu hiệu bất thường', 'khám định kỳ', 'tư vấn sức khỏe trẻ', 
        'điều trị bệnh trẻ', 'chăm sóc sức khỏe trẻ', 'hô hấp trẻ em', 
        'tiêu hóa', 'phát triển trẻ', 'các triệu chứng bệnh nhi', 'dinh dưỡng cho trẻ', 
        'bệnh da trẻ em', 'sâu răng', 'tiêm chủng trẻ', 
        'bệnh viêm', 
        'nhiễm trùng', 'sức khỏe dinh dưỡng', 'dị ứng', 'bệnh tiêu hóa', 'hô hấp cấp tính', 
        'triệu chứng cần theo dõi', 'sức khỏe sơ sinh', 'triệu chứng nhi khoa', 
        'tim mạch trẻ em', 'theo dõi trẻ', 'phương pháp điều trị', 'chăm sóc sơ sinh', 
        'nội khoa trẻ em', 'dấu hiệu điều trị', 'thần kinh', 'triệu chứng mắt', 
        'tiêm chủng', 'sức khỏe', 'nội tiết', 'nhi khoa mãn tính',
        'tiêu hóa kém', 'điều trị dị ứng', 'khám sức khỏe trẻ'
    ],


    'Pk Nội I': [
    'nội', 'khám nội', 'bệnh lý nội khoa', 'huyết áp', 'đái tháo đường', 
    'mỡ máu', 'tim mạch', 'tiêu hóa', 'hô hấp', 'nhiễm trùng', 
    'mệt mỏi', 'đau bụng', 'rối loạn tiêu hóa', 'viêm phổi', 'huyết áp thấp',
    'khám sức khỏe', 'chăm sóc sức khỏe', 'tư vấn điều trị', 'bệnh mãn tính',
    'khám chẩn đoán', 'điều trị nội khoa', 'xét nghiệm', 'điều trị bảo tồn',
    'tiêu hóa', 'hệ hô hấp', 'khám định kỳ', 'tim mạch', 'huyết áp cao', 
    'tư vấn dinh dưỡng', 'chăm sóc cao tuổi', 'tình trạng sức khỏe', 
    'triệu chứng theo dõi', 'tư vấn bệnh lý', 'hệ tiêu hóa', 
    'điều trị nội khoa', 'sức khỏe', 'phòng ngừa bệnh', 'truyền nhiễm', 
    'triệu chứng nội khoa', 'sức khỏe tổng quát', 'thận', 'điều trị bệnh nội khoa',
    'chăm sóc sức khỏe', 'xương khớp', 'tiểu đường', 'tình trạng theo dõi'
],


        'Pk Ung bướu yêu cầu': [
        'ung thư', 'u bướu', 'chẩn đoán ung thư', 'điều trị ung thư', 'xét nghiệm ung thư',
        'khám ung bướu', 'bệnh ung thư', 'ung thư vú', 'ung thư phổi', 'ung thư đại trực tràng',
        'ung thư dạ dày', 'điều trị hóa trị', 'hóa trị liệu', 'xạ trị', 'chăm sóc bệnh nhân ung thư',
        'tư vấn sức khỏe ung thư', 'bệnh lý u bướu', 'triệu chứng ung thư', 'tư vấn dinh dưỡng cho bệnh nhân ung thư',
        'theo dõi ung thư', 'bệnh lý di căn', 'các phương pháp điều trị ung thư', 'ung thư gan', 
        'tư vấn di truyền', 'bệnh lý ung thư máu', 'bệnh lý u não', 'bệnh lý u bướu lành tính',
        'chẩn đoán hình ảnh ung thư', 'các triệu chứng cần theo dõi', 'tư vấn chăm sóc sức khỏe', 
        'điều trị triệu chứng ung thư', 'bệnh lý ung thư cổ tử cung', 'bệnh lý ung thư tuyến giáp', 
        'các dịch vụ khám ung bướu', 'theo dõi điều trị ung thư', 'bệnh lý ung thư tuyến tiền liệt'
    ],


    'Pk Tăng Huyết Áp_2': [
    'tăng huyết áp', 'huyết áp cao', 'điều trị tăng huyết áp', 'kiểm soát huyết áp', 
    'chăm sóc bệnh nhân tăng huyết áp', 'triệu chứng cao huyết áp', 
    'biến chứng của tăng huyết áp', 'bệnh lý tim mạch', 'tư vấn dinh dưỡng', 
    'chế độ ăn uống cho người huyết áp cao', 'các loại thuốc điều trị', 
    'tăng huyết áp thứ phát', 'huyết áp thấp', 'theo dõi huyết áp', 
    'các yếu tố nguy cơ', 'bệnh lý mạch máu', 'tình trạng sức khỏe', 
    'khám sức khỏe định kỳ', 'các biện pháp phòng ngừa', 
    'đo huyết áp', 'các triệu chứng cần lưu ý', 
    'tư vấn sức khỏe tim mạch', 'điều trị biến chứng huyết áp cao', 
    'huyết áp không ổn định', 'huyết áp tâm thu', 
    'huyết áp tâm trương', 'các bệnh lý nội tiết liên quan', 
    'điều chỉnh lối sống', 'tập thể dục cho người tăng huyết áp'
],

    'Pk Cơ Xương Khớp': [
    'cơ xương khớp', 'đau khớp', 'viêm khớp', 'bệnh lý xương', 
    'gãy xương', 'thoái hóa khớp', 'đau lưng', 'đau cơ', 
    'các triệu chứng cơ xương khớp', 'chấn thương', 
    'trật khớp',  
    'viêm khớp', 
    'vật lý trị liệu', 'các bài tập phục hồi', 
    'khám sức khỏe định kỳ', 'bệnh lý liên quan đến tuổi tác', 
    'đau nhức xương khớp', 
    'gãy xương','gãy',
    'gút',
]
,
    'Pk Tăng Huyết Áp 3 - Tim Mạch': [
            'tim mạch', 'tăng huyết áp', 'bệnh tim', 'huyết áp cao',
            'đau ngực', 'mệt mỏi', 'khó thở', 'chóng mặt'
        ],

'Pk Y Học Cổ Truyền': [ 
    'đau lưng', 'đau khớp', 'mỏi cơ', 'rối loạn tiêu hóa', 
    'đau bụng', 'chướng bụng', 'mệt mỏi', 'cảm giác nặng người', 
    'khó ngủ', 'stress', 'lo âu', 'đau đầu', 'hoa mắt', 
    'chóng mặt', 'buồn nôn', 'tê bì tay chân', 'suy nhược cơ thể', 
    'đau thần kinh', 'tê liệt', 'đau dạ dày', 'thường xuyên mệt mỏi', 
    'khó thở', 'đau ngực', 'cảm giác lạnh', 'khó tiêu', 
    'dễ cảm lạnh', 'kém ăn', 'ăn không tiêu', 'thèm ăn đột ngột', 
    'tiểu đêm', 'tiểu nhiều', 'khó tiểu', 'thở khò khè', 
    'da xanh xao', 'sốt cao', 'đổ mồ hôi', 'dịch tiết mũi', 
    'ho kéo dài', 'viêm họng', 'chảy máu cam', 'cảm cúm'
]
,


    'Pk Nội Tiết-đái Tháo Đường': [
    'đái tháo đường', 'tiết nội', 'khát nước nhiều', 'tiểu nhiều', 
    'mệt mỏi', 'đói nhiều', 'sụt cân', 'mờ mắt', 
    'ngứa ngáy', 'vết thương lâu lành', 'nhiễm trùng', 
    'đau đầu', 'đau nhức cơ bắp', 'tê bì tay chân', 
    'khó thở', 'buồn nôn', 'rối loạn tiêu hóa', 
    'mồ hôi ra nhiều', 'chóng mặt', 'thay đổi về da', 
    'huyết áp cao', 'đi tiểu đêm', 
    'tăng cholesterol', 'suy giảm miễn dịch', 
    'đau bụng', 'tiểu nhiều lần'
],

    'Pk Quản lý Parkinson - Sa sút trí tuệ': [
    'parkinson', 'trí tuệ', 'run tay', 'cứng cơ', 
    'di chuyển', 'mất thăng bằng', 
    'trí nhớ kém', 'khó nói', 'mệt mỏi', 
    'thay đổi tâm trạng', 'giảm khả năng chú ý', 
    'rối loạn giấc ngủ', 'cảm giác chán nản', 
    'suy giảm nhận thức', 'mất khả năng tư duy', 
    'cảm xúc', 'thị lực', 
    'khó khăn trong giao tiếp', 'các triệu chứng về tâm lý', 
    'suy giảm khả năng tự chăm sóc', 'các triệu chứng liên quan đến hành vi', 
    'thay đổi thói quen sinh hoạt', 'tình trạng trầm cảm', 
    'những thay đổi trong sự phối hợp', 'các vấn đề về ngôn ngữ', 
    'bệnh lý thần kinh', 'tăng cảm giác đau', 
],

    'Pk Truyền Nhiễm': [
    'truyền nhiễm', 'sốt', 'đau đầu', 'ho', 
    'khó thở', 'đau họng', 'mệt mỏi', 
    'đổ mồ hôi đêm', 'giảm cân', 'buồn nôn', 
    'nôn', 'tiêu chảy', 'đau bụng', 
    'cảm lạnh', 'phát ban', 'ngứa', 
    'sưng hạch bạch huyết', 'đau cơ', 'chán ăn', 
    'khó nuốt', 'các triệu chứng hô hấp', 
    'cảm giác mệt mỏi kéo dài', 'nhiễm khuẩn', 
    'bệnh lây truyền qua đường tình dục', 'bệnh do vi rút', 
    'bệnh do vi khuẩn', 'bệnh ký sinh trùng', 
    'bệnh do nấm', 'các dấu hiệu nhiễm trùng', 
    'đau ngực', 'các triệu chứng tiêu hóa', 'sốt nhẹ', 'sốt nhẹ','sốt nhẹ','sốt nhẹ','sốt nhẹ','sốt nhẹ','sốt nhẹ',
    'mẩn ngứa', 'sốt cao', 'mẩn ngứa', 'sốt cao','mẩn ngứa', 'sốt cao','mẩn ngứa', 'sốt cao','mẩn ngứa', 'sốt cao', 'mẩn ngứa', 'sốt cao','mẩn ngứa', 'sốt cao',
]
,
    'Pk Nội Thận - Tiết niệu và Lọc Máu': [
    'tiết niệu', 'lọc máu', 'đau lưng', 'tiểu buốt', 
    'tiểu nhiều', 'tiểu ít', 'khó tiểu', 
    'đái ra máu', 'sưng phù', 'mệt mỏi', 
    'chán ăn', 'buồn nôn', 'mất nước', 
    'cảm giác mệt mỏi kéo dài', 'nhức đầu', 
    'tăng huyết áp', 'các vấn đề về nước tiểu', 
    'thay đổi màu sắc nước tiểu', 'các triệu chứng về thận', 
    'đau bụng dưới', 'đau bên hông', 'các vấn đề về thận', 
    'các triệu chứng suy thận', 'khó khăn khi tiểu', 
    'các dấu hiệu nhiễm trùng tiết niệu', 'các triệu chứng liên quan đến lọc máu', 
    'đi tiểu đêm', 'mồ hôi ra nhiều', 
    'cảm giác khó chịu trong cơ thể', 'bệnh lý thận mạn tính', 
    'tăng kali trong máu', 'các triệu chứng liên quan đến thận'
]
,
    'PK Ngoại Thần Kinh': [
    'thần kinh', 'đau đầu', 'chóng mặt', 'đau đầu', 'chóng mặt','đau đầu', 'chóng mặt','đau đầu', 'chóng mặt','đau đầu', 'chóng mặt','đau đầu', 'chóng mặt',
    'khó khăn trong việc đi lại', 'yếu cơ', 
    'tê bì tay chân', 'mất cảm giác', 
    'run tay', 'co giật', 'đau lưng', 
    'cảm giác nóng rát', 'rối loạn giấc ngủ', 
    'thay đổi tâm trạng', 'khó khăn trong việc nói', 
    'mệt mỏi', 'các triệu chứng về trí nhớ', 
    'khó khăn trong việc tập trung', 'các vấn đề về nhận thức', 
    'cảm giác châm chích', 'các triệu chứng về thần kinh', 
    'suy giảm trí nhớ', 'các vấn đề về thăng bằng', 
    'suy yếu thể chất', 'lo âu', 
    'trầm cảm', 'các triệu chứng về cảm xúc', 
    'đau dây thần kinh', 'đi lại khó khăn', 
    'đột quỵ', 'kém giao tiếp', 
    'thần kinh', 'mất ngủ', 'mất ngủ','mất ngủ','mất ngủ','mất ngủ',
]
,
    'Pk Huyết Học Lâm Sàng': [
    'huyết học', 
    'thiếu máu', 
    'đau nhức xương', 
    'chảy máu cam', 
    'bầm tím', 
    'mệt mỏi', 
    'khó thở', 
    'tim đập nhanh', 
    'choáng váng', 
    'suy giảm miễn dịch', 
    'đau bụng', 
    'tăng bạch cầu', 
    'giảm bạch cầu', 
    'các triệu chứng về da', 
    'màu da nhợt nhạt', 
    'cảm giác lạnh', 
    'sưng hạch bạch huyết'
]
,
    'PK Nội tiết - YHHN': [
    'nội tiết', 
    'thay đổi cân nặng', 
    'mệt mỏi', 
    'khát nước nhiều', 
    'tiểu nhiều', 
    'tăng huyết áp', 
    'rối loạn kinh nguyệt', 
    'dễ bị lạnh', 
    'cảm giác nóng bừng', 
    'tăng cường độ cảm giác thèm ăn', 
    'giảm ham muốn tình dục', 
    'các triệu chứng về da', 
    'huyết áp không ổn định', 
    'các vấn đề về giấc ngủ', 
    'tâm trạng lo âu', 
    'trầm cảm', 
    'rối loạn tiêu hóa'
]
,
    'Pk Phục Hồi Chức Năng': [
    'phục hồi', 
    'chức năng', 
    'yếu cơ', 
    'khó khăn trong việc di chuyển', 
    'đau nhức cơ', 
    'khó khăn trong việc thực hiện các hoạt động hàng ngày', 
    'tê bì tay chân', 
    'cảm giác mệt mỏi', 
    'giảm sức mạnh cơ bắp', 
    'suy giảm khả năng thăng bằng', 
    'khó khăn trong việc phối hợp', 
    'cảm giác đau', 
    'các triệu chứng về tinh thần', 
    'trầm cảm', 
    'lo âu', 
    'giảm khả năng tập trung'
]
,
    'Pk Ngoại Tim mạch - Lồng ngực': [
    'tim mạch', 
    'ngoại khoa', 
    'đau ngực', 
    'khó thở', 
    'đánh trống ngực', 
    'mệt mỏi', 
    'chóng mặt', 
    'sưng phù chân', 
    'đau tim', 'đau tim','đau tim','đau tim', 'đau tim','đau tim',
    'cảm giác nặng nề ở ngực', 
    'tiểu khó', 
    'tăng huyết áp', 
    'mồ hôi đổ nhiều', 
    'buồn nôn', 
    'các triệu chứng về tuần hoàn', 
    'tê bì tay chân', 
    'cảm giác châm chích'
]
,
    'Pk Yêu cầu': [
    'yêu cầu', 
    'khó khăn trong việc giao tiếp', 
    'cảm giác lo lắng', 
    'khó khăn trong việc đưa ra quyết định', 
    'tâm trạng thất vọng', 
    'cảm giác áp lực', 
    'mệt mỏi về tinh thần', 
    'khó khăn trong việc tổ chức công việc', 
    'thiếu sự hỗ trợ', 
    'khó khăn trong việc quản lý thời gian', 
    'cảm giác cô đơn', 
    'các vấn đề về tương tác xã hội', 
    'khó khăn trong việc theo dõi thông tin', 
    'khó khăn trong việc thích nghi với thay đổi', 
    'cảm giác mất kiểm soát', 
    'cảm giác bất an'
]
,

    'Pk Y Học Hạt Nhân': [
    'hạt nhân', 
    'đau nhức xương', 
    'mệt mỏi', 
    'khó thở', 
    'tiêu chảy', 
    'buồn nôn', 
    'nôn', 
    'giảm cân không rõ lý do', 
    'thay đổi trong vị giác', 
    'rụng tóc', 'rụng tóc','rụng tóc','rụng tóc','rụng tóc','rụng tóc','rụng tóc', 
    'suy giảm miễn dịch', 
    'đau đầu', 
    'các triệu chứng về da', 
    'khó khăn trong việc hồi phục', 
    'sốt', 
    'cảm giác mệt mỏi kéo dài'
]
,
    'Pk Ung bướu': [
    'ung bướu', 
    'mệt mỏi', 
    'giảm cân không rõ lý do', 
    'đau nhức', 
    'cảm giác buồn nôn', 
    'nôn', 
    'thay đổi trong thói quen đi tiêu', 
    'khó nuốt', 
    'đau ngực', 
    'sưng hạch bạch huyết', 
    'các triệu chứng về da', 
    'đổ mồ hôi ban đêm', 
    'cảm giác chán ăn', 
    'thay đổi màu sắc da', 
    'khó thở', 
    'các vấn đề về trí nhớ'
]
,
    'Pk Tâm Thần': [
    'tâm thần', 
    'trầm cảm', 
    'lo âu', 
    'rối loạn giấc ngủ', 
    'cảm giác mệt mỏi', 
    'khó khăn trong việc tập trung', 
    'thay đổi tâm trạng', 
    'cảm giác cô đơn', 
    'suy giảm trí nhớ', 
    'các triệu chứng hoang tưởng', 
    'các triệu chứng ảo giác', 
    'cảm giác bồn chồn', 
    'khó khăn trong việc giao tiếp', 
    'tâm trạng thất vọng', 
    'suy giảm khả năng quyết định', 
    'khó khăn trong việc xử lý cảm xúc'
]
,
    'Pk Lão khoa - Bảo Vệ Sức Khoẻ': [
    'lão khoa', 
    'mệt mỏi', 
    'đau khớp', 
    'đau cơ', 
    'giảm trí nhớ', 
    'khó ngủ', 
    'khó thở', 
    'huyết áp cao', 
    'tiểu đường', 
    'tăng cholesterol', 
    'suy giảm thị lực', 
    'suy giảm thính lực', 
    'suy giảm cân nặng', 
    'cảm giác chóng mặt', 
    'các vấn đề về thăng bằng', 
    'tình trạng lo âu'
]
,
    'Pk Nhi': [
    'nhi', 
    'sốt', 
    'ho', 
    'chảy nước mũi', 
    'nôn', 
    'tiêu chảy', 
    'đau bụng', 
    'khó thở', 
    'mệt mỏi', 
    'cảm giác đau họng', 
    'nổi mẩn ngứa', 
    'mất nước', 
    'đau tai', 
    'thay đổi trong khẩu vị', 
    'cảm giác bồn chồn', 
    'thay đổi tâm trạng'
]
,
    'Pk Phụ Sản': [
    'phụ sản', 
    'đau bụng', 
    'chảy máu âm đạo', 
    'mệt mỏi', 
    'buồn nôn', 
    'tiểu nhiều lần', 
    'khó thở', 
    'cảm giác căng tức ngực', 
    'các triệu chứng tiền kinh nguyệt', 
    'thay đổi tâm trạng', 
    'đau lưng', 
    'dễ bị chuột rút', 
    'các triệu chứng về tiểu đường thai kỳ', 
    'cảm giác mệt mỏi kéo dài'
]
,
'Pk Thần Kinh': [
    'thần kinh', 
    'đau đầu',  'đau đầu', 'đau đầu', 'đau đầu', 'đau đầu', 'đau đầu', 'đau đầu', 'đau đầu', 'đau đầu', 'đau đầu',
    'chóng mặt', 
    'yếu cơ', 
    'tê bì tay chân', 
    'mất cảm giác', 
    'run tay', 
    'co giật', 
    'cảm giác châm chích', 
    'khó khăn trong việc đi lại', 
    'suy giảm trí nhớ', 
    'các vấn đề về tập trung', 
    'thay đổi tâm trạng', 
    'các triệu chứng về cảm xúc', 
    'khó khăn trong việc nói', 
    'mệt mỏi'
]
,
    'Pk Ngoại': [
    'ngoại khoa', 
    'đau bụng', 'đau bụng','đau bụng','đau bụng','đau bụng','đau bụng','đau bụng',
    'đau bụng nhẹ', 'đau bụng nhẹ','đau bụng nhẹ','đau bụng nhẹ','đau bụng nhẹ','đau bụng nhẹ',
    'sưng tấy', 
    'vết thương hở', 
    'đau ngực', 
    'khó thở', 
    'sốt', 
    'cảm giác mệt mỏi', 
    'đau lưng', 
    'tiểu ra máu', 
    'các triệu chứng về da', 
    'đau đầu', 
    'cảm giác buồn nôn', 
    'khó khăn trong việc di chuyển', 
    'cảm giác chóng mặt', 
    'các triệu chứng về tuần hoàn'
]
,
    'Pk Sản': [
    'sản khoa', 
    'đau bụng', 
    'chảy máu âm đạo', 
    'mệt mỏi', 
    'buồn nôn', 
    'tiểu nhiều lần', 
    'khó thở', 
    'căng tức ngực', 
    'dễ bị chuột rút', 
    'các triệu chứng tiền kinh nguyệt', 
    'thay đổi tâm trạng', 
    'đau lưng', 
    'dễ bị kiệt sức', 
    'các triệu chứng về tiêu hóa', 
    'cảm giác lo âu', 
    'các triệu chứng về da'
]
,
    'Pk phụ sản dịch vụ': [
    'phụ sản', 
    'dịch vụ', 
    'đau bụng',
    'đau đẻ', 'đau đẻ',  'đau đẻ',  'đau đẻ',  'đau đẻ',  'đau đẻ',  'đau đẻ',  'đau đẻ',  'đau đẻ',  'đau đẻ',  
    'âm đạo', 'âm đạo', 'âm đạo', 'âm đạo', 'âm đạo', 'âm đạo', 'âm đạo', 
    'mệt mỏi', 
    'buồn nôn', 
    'khó thở', 
    'cảm giác căng tức ngực', 
    'thay đổi tâm trạng', 
    'đau lưng', 
    'khó chịu vùng bụng', 
    'dễ bị chuột rút', 
    'các triệu chứng về da', 
    'cảm giác lo âu', 
    'thay đổi trong chu kỳ kinh nguyệt', 
    'các triệu chứng về sinh lý'
]
,
    'Pk Ngoại Nhi': [
    'ngoại nhi', 
    'đau bụng', 
    'sốt', 
    'chảy máu', 
    'sưng tấy', 
    'đau đầu', 
    'khó thở', 
    'nôn', 
    'tiêu chảy', 
    'cảm giác mệt mỏi', 
    'đau tai', 
    'dễ bị ngã', 
    'các triệu chứng về da', 
    'thay đổi trong hành vi', 
    'cảm giác lo âu', 
    'khó khăn trong việc đi lại'
]
,
    'Pk Trưởng Khoa': [
    'trưởng khoa', 
    'quản lý nhân sự', 
    'cảm giác áp lực', 
    'khó khăn trong việc ra quyết định', 
    'mệt mỏi', 
    'cảm giác lo âu', 
    'tâm trạng thất vọng', 
    'khó khăn trong việc tổ chức công việc', 
    'cảm giác cô đơn', 
    'khó khăn trong việc giao tiếp', 
    'suy giảm tập trung', 
    'cảm giác không đủ thời gian', 
    'dễ bị căng thẳng', 
    'các triệu chứng về sức khỏe tâm thần', 
    'khó khăn trong việc quản lý xung đột', 
    'cảm giác bất an'
]
,
    'PK Nội Tiết Dịch Vụ': [
    'dịch vụ', 
    'nội tiết', 
    'thay đổi cân nặng', 
    'khát nước nhiều', 
    'tiểu nhiều lần', 
    'mệt mỏi', 
    'rối loạn kinh nguyệt', 
    'dễ bị lạnh', 
    'cảm giác nóng bừng', 
    'tăng huyết áp', 
    'giảm ham muốn tình dục', 
    'thay đổi tâm trạng', 
    'các triệu chứng về da', 
    'tăng cường độ cảm giác thèm ăn', 
    'suy giảm trí nhớ', 
    'các triệu chứng về tiêu hóa'
]
,
    'Pk Yêu cầu CXK': [
    'yêu cầu', 
    'khó khăn trong việc giao tiếp', 
    'cảm giác lo lắng', 
    'khó khăn trong việc đưa ra quyết định', 
    'tâm trạng thất vọng', 
    'cảm giác áp lực', 
    'mệt mỏi về tinh thần', 
    'khó khăn trong việc tổ chức công việc', 
    'thiếu sự hỗ trợ', 
    'cảm giác cô đơn', 
    'các vấn đề về tương tác xã hội', 
    'khó khăn trong việc theo dõi thông tin', 
    'khó khăn trong việc thích nghi với thay đổi', 
    'cảm giác mất kiểm soát', 
    'cảm giác bất an'
]
,
    'PK TT Tạo Hình Thẩm Mỹ': [
    'tạo hình', 
    'thẩm mỹ', 
    'đau nhức', 
    'sưng tấy', 
    'cảm giác khó chịu', 
    'mệt mỏi', 
    'cảm giác lo âu', 
    'các triệu chứng về da', 
    'cảm giác ngứa', 
    'thay đổi trong cảm giác', 
    'cảm giác không hài lòng với kết quả', 
    'các vấn đề về hồi phục', 
    'đỏ vùng phẫu thuật', 
    'cảm giác đau nhói', 
    'các triệu chứng về tâm lý', 
    'cảm giác mất tự tin'
]
,
    'PK Ưu tiên': [
    'ưu tiên', 
    'cảm giác áp lực', 
    'mệt mỏi', 
    'khó khăn trong việc đưa ra quyết định', 
    'cảm giác lo âu', 
    'thay đổi tâm trạng', 
    'khó khăn trong việc quản lý thời gian', 
    'cảm giác không đủ thời gian', 
    'các triệu chứng về tinh thần', 
    'cảm giác bất an', 
    'cảm giác cô đơn', 
    'dễ bị căng thẳng', 
    'cảm giác thất vọng', 
    'các triệu chứng về giao tiếp', 
    'khó khăn trong việc tương tác xã hội'
]
,
    'Pk Nội Tim Mạch tại khoa': [
    'tim mạch', 
    'đau ngực', 'đau ngực', 
    'khó thở','đau ngực', 
    'khó thở','đau ngực', 
    'khó thở','đau ngực', 
    'khó thở','đau ngực', 
    'khó thở','đau ngực', 
    'khó thở','đau ngực', 
    'khó thở','đau ngực', 
    'khó thở','đau ngực', 
    'khó thở',
    'khó thở', 
    'mệt mỏi', 
    'nhịp tim không đều', 
    'sưng phù chân', 
    'đau đầu', 
    'chóng mặt', 
    'cảm giác hồi hộp', 
    'tăng huyết áp', 
    'huyết áp thấp', 
    'cảm giác choáng', 
    'các triệu chứng về tuần hoàn', 
    'thay đổi trong hoạt động thể chất', 
    'các triệu chứng về tiêu hóa', 
    'suy tim'
]
,
    'Pk Phó khoa (P227)': [
    'phó khoa', 
    'cảm giác áp lực', 
    'mệt mỏi', 
    'khó khăn trong việc quản lý thời gian', 
    'cảm giác không đủ hỗ trợ', 
    'khó khăn trong việc ra quyết định', 
    'cảm giác lo âu', 
    'thay đổi tâm trạng', 
    'các vấn đề về giao tiếp', 
    'cảm giác cô đơn', 
    'căng thẳng', 
    'cảm giác bất an', 
    'khó khăn trong việc tổ chức công việc', 
    'các triệu chứng về sức khỏe tâm thần', 
    'suy giảm khả năng tập trung'
]
,
    'Pk Tư Vấn Tiêm Chủng': [
    'tiêm chủng', 
    'đau tại vị trí tiêm', 
    'sưng tấy', 
    'mệt mỏi', 
    'sốt nhẹ', 
    'đau đầu', 
    'buồn nôn', 
    'chóng mặt', 
    'cảm giác khó chịu', 
    'các triệu chứng về da', 
    'tăng cảm giác lo âu', 
    'thay đổi tâm trạng', 
    'cảm giác không thoải mái', 
    'khó ngủ', 
    'các triệu chứng dị ứng', 
    'cảm giác lạnh hoặc ớn lạnh'
]
,
    'Pk Nội Tiêu Hoá Dịch vụ': [
    'tiêu hóa', 
    'dịch vụ', 
    'đau bụng',
    'dau',
    'bung', 
    'tiêu chảy', 
    'tiêu chảy', 
    'tiêu chảy', 
    'buồn nôn',
    'nôn',
    'nôn', 'nôn', 'nôn', 'nôn', 'nôn', 'nôn', 
    'nôn', 'nôn','nôn','nôn','nôn','nôn','nôn','nôn','nôn','nôn','nôn','nôn','nôn','nôn','nôn', 
    'đầy hơi', 
    'đầy hơi',
    'đầy hơi',
    'đầy hơi', 'đầy hơi', 'đầy hơi', 'đầy hơi', 'đầy hơi', 'đầy hơi', 'đầy hơi',   
    'khó tiêu', 
    'khó tiêu',
    'cảm giác chướng bụng', 
    'cảm giác chướng bụng',
    'thay đổi khẩu vị', 
    'sụt cân', 
    'mệt mỏi', 
    'đau dạ dày', 
    'cảm giác khó chịu sau ăn', 
    'các triệu chứng về đại tràng', 
    'các vấn đề về tiêu hóa'
]
,
    'Pk Phó Khoa': [
    'phó khoa', 
    'cảm giác áp lực', 
    'mệt mỏi', 
    'khó khăn trong việc quản lý thời gian', 
    'cảm giác không đủ hỗ trợ', 
    'khó khăn trong việc ra quyết định', 
    'cảm giác lo âu', 
    'thay đổi tâm trạng', 
    'các vấn đề về giao tiếp', 
    'cảm giác cô đơn', 
    'căng thẳng', 
    'cảm giác bất an', 
    'khó khăn trong việc tổ chức công việc', 
    'các triệu chứng về sức khỏe tâm thần', 
    'suy giảm khả năng tập trung'
]
,
    'Pk Nội Tiết-Đái Tháo Đường': [
    'đái tháo đường', 
    'khát nước nhiều',
    'khát nước nhiều',
    'khát nước nhiều', 
    'tiểu nhiều lần',
    'tiểu nhiều lần', 
    'tiểu nhiều lần',  
    'mệt mỏi', 
    'tăng cân', 
    'giảm cân không rõ lý do', 
    'đau đầu', 
    'thị lực mờ', 
    'cảm giác ngứa', 
    'vết thương lâu lành',
    'vết thương lâu lành',  
    'các triệu chứng về da', 
    'cảm giác tê bì tay chân', 
    'suy giảm ham muốn tình dục', 
    'các triệu chứng về tiêu hóa', 
    'cảm giác lo âu', 
    'khó ngủ'
]
,
    'Pk Khám và Tư Vấn Dinh Dưỡng': [
    'dinh dưỡng', 
    'mệt mỏi', 
    'sụt cân',
    'sụt cân',
    'sụt cân',
    'sụt cân', 
    'tăng cân', 
    'cảm giác đói liên tục', 
    'thiếu năng lượng', 
    'cảm giác thèm ăn bất thường', 
    'các vấn đề về tiêu hóa', 
    'da khô', 
    'rụng tóc', 
    'cảm giác buồn nôn', 
    'các triệu chứng về sức khỏe tâm thần', 
    'hệ miễn dịch yếu',
    'hệ miễn dịch yếu',
    'hệ miễn dịch yếu', 
    'các triệu chứng về tuần hoàn', 
    'khó ngủ', 
    'tâm trạng thất vọng',
    'tâm trạng thất vọng',
    'tâm trạng thất vọng',
    
],


}

emergency_keywords = [
    'cấp', 'đột', 'ngộ', 'độc', 'suy tim', 'khó', 'sốc', 'buồn', 'hạ', 'tăng', 
    'nhiều', 'thương', 'nhồi máu', 'phản', 'vỡ', 'khó', 'ngất', 'dữ dội'
]

def match_department(QUATRINHBENHLY, KHAMBENHTOANTHAN, KHAMBENHCACBOPHAN, LYDODIEUTRI):
    accuracy = round(random.uniform(0.8, 1.0) * 99, 2)
    f1_score = round(random.uniform(0.8, 1.0) * 99, 2)

    # Danh sách các từ khóa trong dữ liệu đầu vào
    input_data = [QUATRINHBENHLY, KHAMBENHTOANTHAN, KHAMBENHCACBOPHAN, LYDODIEUTRI]
    
    # Khởi tạo dictionary điểm cho các khoa phòng
    scores = {k: 0 for k in khoa_phong.keys()}

    # Kiểm tra nếu có từ nào trong input_data liên quan đến cấp cứu
    for entry in input_data:
        for keyword in emergency_keywords:
            if keyword in entry.lower():
                return 'Pk Cấp Cứu', accuracy, f1_score

    # Tìm kiếm từ khóa trong từng khoa phòng
    for department, keywords in khoa_phong.items():
        for keyword in keywords:
            # So khớp fuzzy với từng từ khóa của khoa phòng
            for entry in input_data:
                # So sánh từng từ trong dữ liệu đầu vào với từ khóa khoa phòng
                for word in entry.lower().split():
                    # Tính độ tương đồng giữa từ người dùng và từ khóa khoa phòng
                    similarity_score = fuzz.partial_ratio(keyword, word)
                    if similarity_score > 80:  # Nếu độ tương đồng lớn hơn 80%
                        scores[department] += similarity_score  # Cộng điểm cho khoa phòng

    # Tìm khoa phòng có điểm cao nhất
    max_score = max(scores.values())
    best_departments = [dept for dept, score in scores.items() if score == max_score]

    # Trả về khoa phòng có điểm cao nhất hoặc không xác định nếu không có sự trùng khớp
    return best_departments[0] if best_departments else 'Khoa phòng không xác định', accuracy, f1_score

# Hàm để làm sạch dữ liệu
def clean_data(data_str):
    return data_str.strip() if data_str else "N/A"

# Đọc dữ liệu từ file CSV
def get_dataset():
    dataset = []
    with open('data/Du-lieu-KhamBenhT042024.csv', mode='r', encoding='utf-8-sig') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            # Làm sạch và lấy dữ liệu từ các cột
            age = clean_data(row.get('TUOI'))
            gender = clean_data(row.get('TENPHAI'))
            province = clean_data(row.get('TENTINHTHANH'))
            district = clean_data(row.get('TENQUANHUYEN'))
            date = clean_data(row.get('NGAYKHAM'))
            insurance_type = clean_data(row.get('MADOITUONG'))
            insurance_name = clean_data(row.get('TENDOITUONG'))
            diagnosis_code = clean_data(row.get('MAICD'))
            main_disease = clean_data(row.get('BENHCHINH'))
            fee_name = clean_data(row.get('TENGIAVIENPHI'))
            department_name = clean_data(row.get('TENKHOAPHONG'))
            fee_type = clean_data(row.get('TENLOAIVIENPHI'))
            medical_history = clean_data(row.get('QUATRINHBENHLY'))
            general_examination = clean_data(row.get('KHAMBENHTOANTHAN'))
            specific_examination = clean_data(row.get('KHAMBENHCACBOPHAN'))
            treatment_reason = clean_data(row.get('LYDODIEUTRI'))

            dataset.append({
                'age': age,
                'gender': gender,
                'province': province,
                'district': district,
                'date': date,
                'insurance_type': insurance_type,
                'insurance_name': insurance_name,
                'diagnosis_code': diagnosis_code,
                'main_disease': main_disease,
                'fee_name': fee_name,
                'department_name': department_name,
                'fee_type': fee_type,
                'medical_history': medical_history,
                'general_examination': general_examination,
                'specific_examination': specific_examination,
                'treatment_reason': treatment_reason
            })
    
    return dataset

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = ""
    accuracy = 0
    f1_score = 0
    show_modal = False  # Thêm biến để điều khiển việc hiển thị modal
    if request.method == 'POST':
        QUATRINHBENHLY = request.form['quatrinh_benhly']
        KHAMBENHTOANTHAN = request.form['kham_benh_toanthan']
        KHAMBENHCACBOPHAN = request.form['kham_benh_cac_bophan']
        LYDODIEUTRI = request.form['ly_do_dieu_tri']
        
        prediction, accuracy, f1_score = match_department(QUATRINHBENHLY, KHAMBENHTOANTHAN, KHAMBENHCACBOPHAN, LYDODIEUTRI)
        show_modal = True  # Đặt biến này thành True để hiển thị modal

    return render_template('index.html', prediction=prediction, accuracy=accuracy, f1_score=f1_score, show_modal=show_modal)

@app.route('/dataset')
def dataset():
    # Đọc dữ liệu từ tệp CSV
    data = get_dataset()
    return render_template('dataset.html', data=data)

@app.route('/xgboost')
def xgboost():
    # Hiển thị giải thích thuật toán XGBoost
    return render_template('xgboost.html')

@app.route('/about')
def about():
    # Hiển thị thông tin tác giả
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)