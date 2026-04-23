from typing import Dict, Any, List, Optional

KPI_DB = {
    "inter_brand_mobility": {
        "value": 0.23,
        "target": 0.40,
        "description": "Tỷ lệ luân chuyển nhân tài giữa các thương hiệu"
    },
    "talent_pipeline_fill_rate": {
        "value": 0.68,
        "target": 0.85,
        "description": "Tỷ lệ lấp đầy vị trí lãnh đạo từ nội bộ"
    },
    "training_completion_rate": {
        "value": 0.45,
        "target": 0.70,
        "description": "Tỷ lệ hoàn thành đào tạo khung năng lực"
    },
    "leadership_satisfaction": {
        "value": 0.71,
        "target": 0.80,
        "description": "Mức độ hài lòng với chương trình phát triển lãnh đạo"
    }
}

COMPETENCY_FRAMEWORK = {
    "Vision": "Khả năng dự đoán xu hướng xa xỉ và thiết lập hướng đi dài hạn",
    "Entrepreneurship": "Khuyến khích sự nhanh nhạy, quyết đoán và tối ưu hóa nguồn lực",
    "Passion": "Sự tận tâm với nghệ thuật thủ công và di sản thương hiệu",
    "Trust": "Xây dựng môi trường chính trực, minh bạch và hợp tác đa văn hóa"
}


REGIONAL_INSIGHTS = {
    "europe": {
        "status": "3/5 brands chưa áp dụng khung năng lực",
        "challenges": ["Ngân sách đào tạo bị đóng băng", "HR địa phương kháng cự", "Áp lực thời gian"],
        "training_needs": ["Hiểu Group DNA", "Áp dụng 360 feedback", "Quản lý thay đổi"]
    },
    "asia_pacific": {
        "status": "Áp dụng nhanh nhưng mức độ trưởng thành khác nhau",
        "challenges": ["Rào cản ngôn ngữ và văn hóa", "Tỷ lệ turnover cao"],
        "training_needs": ["Thích ứng framework với văn hóa địa phương", "Succession planning"]
    },
    "north_america": {
        "status": "Thương hiệu lớn áp dụng tốt hơn",
        "challenges": ["Tập trung vào kết quả ngắn hạn", "Tích hợp với performance management hiện tại"],
        "training_needs": ["Business case cho L&D", "ROI metrics"]
    }
}


def lookup_kpi(kpi_name: str) -> Dict[str, Any]:
    if kpi_name in KPI_DB:
        return KPI_DB[kpi_name]
    return {"error": f"KPI '{kpi_name}' không tồn tại"}


def get_competency_framework(theme: str = "all") -> Dict[str, str]:
    if theme == "all":
        return COMPETENCY_FRAMEWORK
    return {theme: COMPETENCY_FRAMEWORK.get(theme, "Không tìm thấy")}


def get_regional_insights(region: str = "europe") -> Dict[str, Any]:
    region = region.lower()
    if region in REGIONAL_INSIGHTS:
        return REGIONAL_INSIGHTS[region]
    return {"error": f"Region '{region}' không tồn tại"}


def calculate_360_score(scores: Dict[str, float]) -> Dict[str, Any]:
    if not scores:
        return {"error": "Cần cung cấp điểm cho 4 competency"}
    
    total = sum(scores.values())
    average = total / len(scores)
    
    strengths = [k for k, v in scores.items() if v >= 4]
    weaknesses = [k for k, v in scores.items() if v <= 2.5]
    
    return {
        "total": total,
        "average": round(average, 2),
        "strengths": strengths,
        "areas_for_improvement": weaknesses,
        "recommendation": "Tốt" if average >= 4 else "Cần cải thiện" if average < 3 else "Bình thường"
    }


def get_module_info(module_id: str = "module_1") -> Dict[str, Any]:
    modules = {
        "module_1": {
            "name": "Module 1: Xác định vấn đề lãnh đạo & Group DNA",
            "tasks": ["Viết problem statement", "Nói chuyện với CEO", "Nói chuyện với CHRO", "Tạo competency model"]
        },
        "module_2": {
            "name": "Module 2: Thiết kế chương trình 360° + Coaching",
            "tasks": ["Thiết kế blueprint", "Xây dựng participant journey", "Outline coaching program"]
        },
        "module_3": {
            "name": "Module 3: Triển khai và đo lường",
            "tasks": ["Nói chuyện với Regional Manager", "Xây dựng rollout plan", "Tạo measurement plan"]
        }
    }
    return modules.get(module_id, {"error": "Module không tồn tại"})


def get_simulation_progress(current_module: str, completed_tasks: List[str]) -> Dict[str, Any]:
    modules = ["module_1", "module_2", "module_3"]
    current_index = modules.index(current_module) if current_module in modules else 0
    
    return {
        "current_module": current_module,
        "module_index": current_index + 1,
        "total_modules": len(modules),
        "progress_percentage": ((current_index) / len(modules)) * 100,
        "completed_tasks": completed_tasks
    }


def format_kpi_dashboard() -> str:
    lines = ["\nGUCCI GROUP KPI DASHBOARD", "-" * 35]
    for name, data in KPI_DB.items():
        lines.append(f"\n📌 {name.replace('_', ' ').title()}")
        lines.append(f"   Giá trị: {data['value']*100:.0f}%")
        lines.append(f"   Mục tiêu: {data['target']*100:.0f}%")
        lines.append(f"   Khoảng cách: {(data['target'] - data['value'])*100:.0f}%")
    return "\n".join(lines)

TOOLS = {
    "lookup_kpi": lookup_kpi,
    "get_competency_framework": get_competency_framework,
    "get_regional_insights": get_regional_insights,
    "calculate_360_score": calculate_360_score,
    "get_module_info": get_module_info,
    "get_simulation_progress": get_simulation_progress,
    "format_kpi_dashboard": format_kpi_dashboard
}


def execute_tool(tool_name: str, arguments: Dict) -> str:
    """Thực thi tool và trả về kết quả"""
    import json
    
    if tool_name not in TOOLS:
        return json.dumps({"error": f"Tool '{tool_name}' không tồn tại"})
    
    try:
        result = TOOLS[tool_name](**arguments)
        return json.dumps(result, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "lookup_kpi",
            "description": "Tra cứu giá trị KPI hiện tại",
            "parameters": {
                "type": "object",
                "properties": {
                    "kpi_name": {
                        "type": "string",
                        "enum": list(KPI_DB.keys()),
                        "description": "Tên KPI cần tra cứu"
                    }
                },
                "required": ["kpi_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_competency_framework",
            "description": "Lấy thông tin khung năng lực (Vision, Entrepreneurship, Passion, Trust)",
            "parameters": {
                "type": "object",
                "properties": {
                    "theme": {
                        "type": "string",
                        "enum": ["Vision", "Entrepreneurship", "Passion", "Trust", "all"],
                        "description": "Chủ đề năng lực cần lấy"
                    }
                },
                "required": ["theme"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_regional_insights",
            "description": "Lấy thông tin chi tiết về tình hình đào tạo theo khu vực",
            "parameters": {
                "type": "object",
                "properties": {
                    "region": {
                        "type": "string",
                        "enum": ["europe", "asia_pacific", "north_america"],
                        "description": "Khu vực cần lấy thông tin"
                    }
                },
                "required": ["region"]
            }
        }
    }
]