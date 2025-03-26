import React, { useEffect, useState } from "react";
import Header from "../../components/Header";
import Footer from "../../components/Footer";
import Sidebar from "../../components/Sidebar";
import axiosInstance from "../../components/axiosInstance";
import { useNavigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";

const heatHistoryData = [
  { time: "14:00", status: "Bật" },
  { time: "13:00", status: "Tắt" },
  { time: "12:00", status: "Bật" },
  { time: "11:00", status: "Tắt" },
];

const fanHistoryData = [
  { time: "14:00", status: "Bật" },
  { time: "13:00", status: "Tắt" },
  { time: "12:00", status: "Bật" },
  { time: "10:00", status: "Tắt" },
];


const DashboardTempPage = () => {

  const [temperatureBound, setTemperatureBound] = useState({ lowest: null, highest: null });
  const [editing, setEditing] = useState(false);
  const [editValues, setEditValues] = useState({ lowest: "", highest: "" });
  const [currentTemp, setCurrentTemp] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("access_token");
          
    if (!token) {
      navigate("/login");
      return;
    }
  
    let decoded;
    try {
      decoded = jwtDecode(token);
      const now = Date.now() / 1000;
      if (decoded.exp < now) {
        navigate("/login");
        return;
      }
    } catch (err) {
      console.error("Token không hợp lệ:", err);
      navigate("/login");
      return;
    }

    const fetchTempBound = async () => {
      try {
        const res = await axiosInstance.get("/temperature/bound/get/");
        setTemperatureBound({
          lowest: res.data.lowest_allowed,
          highest: res.data.highest_allowed,
        });
      } catch (err) {
        console.error("Lỗi khi tải ngưỡng nhiệt độ:", err);
      }
    };
  
    const fetchCurrentTemp = async () => {
      try {
        // Gửi request sync trước
        await axiosInstance.post("/temperature/record/sync/");
        // Sau đó lấy giá trị mới nhất
        const res = await axiosInstance.get("/temperature/record/get/recent/?n=1");
        if (res.data && res.data.length > 0) {
          setCurrentTemp(res.data[0].value); 
        }
      } catch (err) {
        console.error("Lỗi khi lấy ánh sáng hiện tại:", err);
      }
    };
  
    fetchTempBound();
    fetchCurrentTemp();
  }, [navigate]);

  const handleEditClick = () => {
    setEditValues({
      lowest: temperatureBound.lowest,
      highest: temperatureBound.highest,
    });
    setEditing(true);
  };

  const handleSave = async () => {
    const lowest = parseFloat(editValues.lowest);
    const highest = parseFloat(editValues.highest);



    try {
      const res = await axiosInstance.patch("/api/temperature/bound/update/", {
        lowest_allowed: lowest,
        highest_allowed: highest,
      });

      setTemperatureBound({
        lowest: res.data.lowest_allowed,
        highest: res.data.highest_allowed,
      });

      setEditing(false);
    } catch (err) {
      console.error("Lỗi khi cập nhật:", err);
    }
  };

  const handleChange = (e) => {
    setEditValues({ ...editValues, [e.target.name]: e.target.value });
  };

  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      <div className="flex flex-grow">
        <Sidebar activeItem="temperature" />

        <div className="flex-1 p-6">
          <div className="flex justify-between">
            <div className="w-[60%]">
              <h2 className="text-xl font-bold mb-4">Nhiệt độ hiện tại</h2>
              <div className="w-48 p-4 bg-white border shadow rounded-lg flex items-center">
                <span className="text-2xl mr-2">🌡️</span>
                <div>
                  <p className="text-gray-700">Nhiệt độ</p>
                  <p className="font-bold">
                    {currentTemp !== null ? `${currentTemp}°C` : "Đang tải..."}
                  </p>
                </div>
              </div>
            </div>

            <div className="w-[40%] pr-6">
              <h2 className="text-xl font-bold mb-4">Ngưỡng nhiệt độ cần thiết</h2>
              <div
                className={`grid grid-rows-2 gap-y-2 p-4 border shadow rounded-lg items-center font-bold ${
                  editing ? "bg-yellow-50 border-yellow-500" : "bg-white"
                }`}
              >
                {/* HÀNG TỪ */}
                <div className="flex justify-between items-center">
                  <div className="w-[18%]">Từ</div>
                  <div className="flex-grow mx-1">
                    {editing ? (
                      <div className="border border-yellow-500 rounded px-2 py-1 bg-white">
                        <input
                          type="number"
                          name="lowest"
                          value={editValues.lowest}
                          onChange={handleChange}
                          className="w-full outline-none"
                        />
                      </div>
                    ) : (
                      <div className="bg-gray-300 rounded-sm text-center py-1">
                        {temperatureBound.lowest !== null
                          ? `${temperatureBound.lowest} °C`
                          : "Đang tải..."}
                      </div>
                    )}
                  </div>
                  <div className="w-[26%]"></div>
                </div>

                {/* HÀNG ĐẾN */}
                <div className="flex justify-between items-center">
                  <div className="w-[18%]">Đến</div>
                  <div className="flex-grow mx-1">
                    {editing ? (
                      <div className="border border-yellow-500 rounded px-2 py-1 bg-white">
                        <input
                          type="number"
                          name="highest"
                          value={editValues.highest}
                          onChange={handleChange}
                          className="w-full outline-none"
                        />
                      </div>
                    ) : (
                      <div className="bg-gray-300 rounded-sm text-center py-1">
                        {temperatureBound.highest !== null
                          ? `${temperatureBound.highest} °C`
                          : "Đang tải..."}
                      </div>
                    )}
                  </div>
                  <div className="w-[26%] flex justify-end space-x-2">
                    {editing ? (
                      <>
                        <button
                          className="bg-green-600 text-white text-xs rounded-md px-2 hover:bg-green-700"
                          onClick={handleSave}
                        >
                          Lưu
                        </button>
                        <button
                          className="bg-gray-400 text-white text-xs rounded-md px-2 hover:bg-gray-500"
                          onClick={() => setEditing(false)}
                        >
                          Hủy
                        </button>
                      </>
                    ) : (
                      <button
                        className="bg-[#598868] text-white text-xs hover:bg-green-600 rounded-md px-2"
                        onClick={handleEditClick}
                      >
                        Chỉnh sửa
                      </button>
                    )}
                  </div>
                </div>
              </div>

            </div>
          </div>

          {/* Chế độ điều chỉnh */}
          <h2 className="text-xl font-bold mt-6 mb-2">Chế độ điều chỉnh</h2>
          <div className="grid grid-cols-2 gap-x-2 w-[50%] font-bold">
            <div className="p-4 py-6 bg-white border shadow rounded-lg flex items-center">
              <input type="radio" name="temp-mode" className="mr-2" />
              <p>Thủ công</p>
            </div>
            <div className="p-4 py-6 bg-white border shadow rounded-lg flex items-center">
              <input type="radio" name="temp-mode" className="mr-2" />
              <p>Tự động</p>
            </div>
          </div>

          {/* Điều chỉnh đèn và quạt */}
          <div className="flex justify-between mt-6">
            <div className="w-[48%]">
              <h2 className="text-xl font-bold mb-2">Điều chỉnh đèn sưởi</h2>
              <div className="bg-white border shadow rounded-lg flex items-center p-4 py-6">
                <label className="inline-flex items-center cursor-pointer">
                  <input type="checkbox" className="sr-only peer" />
                  <div className="relative w-11 h-6 bg-gray-400 peer-focus:outline-none peer-focus:ring-1 peer-focus:ring-gray-800 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-green-500"></div>
                  <span className="ms-3 text-sm font-bold">Bật</span>
                </label>
              </div>
            </div>

            <div className="w-[48%]">
              <h2 className="text-xl font-bold mb-2">Điều chỉnh quạt thông gió</h2>
              <div className="bg-white border shadow rounded-lg flex items-center p-4 py-6">
                <label className="inline-flex items-center cursor-pointer">
                  <input type="checkbox" className="sr-only peer" />
                  <div className="relative w-11 h-6 bg-gray-400 peer-focus:outline-none peer-focus:ring-1 peer-focus:ring-gray-800 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-green-500"></div>
                  <span className="ms-3 text-sm font-bold">Bật</span>
                </label>
              </div>
            </div>
          </div>

          {/* Lịch sử hoạt động */}
          <div className="flex justify-between mt-6">
            <div className="w-[48%]">
              <h2 className="text-xl font-bold mb-2">Lịch sử hoạt động đèn sưởi</h2>
              <div className="border rounded-lg shadow-md bg-white">
                {heatHistoryData.map((item, index) => (
                  <div key={index} className="flex items-center px-4 py-3 border-b last:border-none">
                    <span className="mr-2 text-lg">💡</span>
                    <div className="flex-grow">
                      <p className="text-sm font-semibold">Thời gian: {item.time}</p>
                      <p className="text-sm">Trạng thái: {item.status}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="w-[48%]">
              <h2 className="text-xl font-bold mb-2">Lịch sử hoạt động quạt</h2>
              <div className="border rounded-lg shadow-md bg-white">
                {fanHistoryData.map((item, index) => (
                  <div key={index} className="flex items-center px-4 py-3 border-b last:border-none">
                    <span className="mr-2 text-lg">🌀</span>
                    <div className="flex-grow">
                      <p className="text-sm font-semibold">Thời gian: {item.time}</p>
                      <p className="text-sm">Trạng thái: {item.status}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

        </div>
      </div>
      <Footer />
    </div>
  );
};

export default DashboardTempPage;
