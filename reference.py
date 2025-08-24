import re
from typing import List, Dict, Any

def parse_legal_status(status_text: str) -> List[Dict[str, Any]]:
    """
    解析历史法律状态字符串，将不同的法律状态拆分成字典列表
    
    Args:
        status_text: 历史法律状态字符串
        
    Returns:
        List[Dict]: 包含各个法律状态信息的字典列表
    """
    if not status_text or pd.isna(status_text):
        return []
    
    # 按照 # 分割不同的法律状态记录
    status_blocks = [block.strip() for block in status_text.split('#') if block.strip()]
    
    parsed_statuses = []
    
    for block in status_blocks:
        status_dict = {}
        
        # 按行分割每个状态块
        lines = [line.strip() for line in block.split('\n') if line.strip()]
        
        for line in lines:
            if '：' in line:
                key, value = line.split('：', 1)
                key = key.strip()
                value = value.strip().rstrip(';')
                
                # 处理特殊字段
                if key == '法律状态公告日':
                    status_dict['法律状态公告日'] = value
                elif key == '法律状态':
                    status_dict['法律状态'] = value
                elif key == '描述信息':
                    status_dict['描述信息'] = value
                    
                    # 从描述信息中提取更多字段
                    desc_parts = value.split(';')
                    for part in desc_parts:
                        if 'IPC(主分类):' in part:
                            ipc_match = re.search(r'IPC\(主分类\):([^;]+)', part)
                            if ipc_match:
                                status_dict['IPC主分类'] = ipc_match.group(1).strip()
                        
                        elif '变更事项:' in part:
                            change_match = re.search(r'变更事项:([^;]+)', part)
                            if change_match:
                                if '变更事项' not in status_dict:
                                    status_dict['变更事项'] = []
                                status_dict['变更事项'].append(change_match.group(1).strip())
                        
                        elif '变更前权利人:' in part:
                            before_match = re.search(r'变更前权利人:([^;]+)', part)
                            if before_match:
                                if '变更前权利人' not in status_dict:
                                    status_dict['变更前权利人'] = []
                                status_dict['变更前权利人'].append(before_match.group(1).strip())
                        
                        elif '变更后权利人:' in part:
                            after_match = re.search(r'变更后权利人:([^;]+)', part)
                            if after_match:
                                if '变更后权利人' not in status_dict:
                                    status_dict['变更后权利人'] = []
                                status_dict['变更后权利人'].append(after_match.group(1).strip())
                        
                        elif '登记生效日:' in part:
                            effect_match = re.search(r'登记生效日:([^;]+)', part)
                            if effect_match:
                                status_dict['登记生效日'] = effect_match.group(1).strip()
                        
                        elif '授权公告日:' in part:
                            auth_match = re.search(r'授权公告日:([^;]+)', part)
                            if auth_match:
                                status_dict['授权公告日'] = auth_match.group(1).strip()
        
        if status_dict:  # 只添加非空的状态字典
            parsed_statuses.append(status_dict)
    
    return parsed_statuses

# 测试函数
test_status = """#法律状态公告日：20120926;
法律状态：授权;
描述信息：授权;

#法律状态公告日：20121219;
法律状态：专利申请权、专利权的转移;
描述信息：专利权的转移IPC(主分类):A41D   1/00;变更事项:专利权人;变更前权利人:辉能科技股份有限公司;变更后权利人:辉能科技股份有限公司;变更事项:地址;变更前权利人:中国台湾台北县五股乡五工路127号4楼;变更后权利人:中国台湾台北县五股乡五工路127号4楼;变更事项:专利权人;变更前权利人:明瑜创新股份有限公司;变更后权利人:英属开曼群岛商辉能控股股份有限公司;登记生效日:20121116;

#法律状态公告日：20220104;
法律状态：专利权有效期届满;
描述信息：专利权有效期届满IPC(主分类):A41D1/00;授权公告日:20120926;"""

print("测试解析函数:")
parsed_result = parse_legal_status(test_status)
for i, status in enumerate(parsed_result):
    print(f"\n法律状态 {i+1}:")
    for key, value in status.items():
        print(f"  {key}: {value}")
