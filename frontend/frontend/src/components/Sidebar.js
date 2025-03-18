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
          <a className="block" href="/dashboard/light">
            Ánh sáng
          </a>
        </li>
        <li className="py-3 pl-4 hover:bg-green-600 cursor-pointer rounded-lg">
          <a className="block" href="/dashboard/temperature">
            Nhiệt độ
          </a>
        </li>
        <li className="py-3 pl-4 hover:bg-green-600 cursor-pointer rounded-lg">
          <a className="block" href="/dashboard/humidity">
            Độ ẩm
          </a>
        </li>
        <li className="py-3 pl-4 hover:bg-green-600 cursor-pointer rounded-lg">
          <a className="block" href="/dashboard/disease-status">
            Tình trạng sâu bệnh
          </a>
        </li>
      </ul>
    </div>
  );
};

export default Sidebar;