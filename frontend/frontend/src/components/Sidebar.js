import React from "react";

const Sidebar = () => {
  return (
    <div className="w-1/6 bg-[#598868] text-white p-2">
      <ul className="w-full">
        <li className="py-3 pl-4 hover:bg-green-600 cursor-pointer rounded-lg">
          Thông báo chung
        </li>
        <li className="py-3 pl-4 bg-gray-300 text-black rounded-lg">
          Tổng quan thông số
        </li>
        <li className="py-3 pl-4 hover:bg-green-600 cursor-pointer rounded-lg">
          Ánh sáng
        </li>
        <li className="py-3 pl-4 hover:bg-green-600 cursor-pointer rounded-lg">
          Nhiệt độ
        </li>
        <li className="py-3 pl-4 hover:bg-green-600 cursor-pointer rounded-lg">
          Độ ẩm
        </li>
        <li className="py-3 pl-4 hover:bg-green-600 cursor-pointer rounded-lg">
          Tình trạng sâu bệnh
        </li>
      </ul>
    </div>
  );
};

export default Sidebar;