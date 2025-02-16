#include<iostream>  
#include<vector>
#include<unordered_map>

using namespace std;

vector<vector<int>> twoSum(vector<int>& nums, int target) {
  unordered_map<int, vector<int>> numMap;
  vector<vector<int>> result;
  for(int i = 0; i < nums.size(); i++){
    int complement = target - nums[i];
    if(numMap.find(complement) != numMap.end()){
      for(int j = 0; j < numMap[complement].size(); j++){
        result.push_back({numMap[complement][j], i});
      }
    }
    numMap[nums[i]].push_back(i);
  }
  return result;
}

int main(){
  int n, target;
    cout << "Nhập số phần tử của mảng: ";
    cin >> n;
    vector<int> nums(n);
    
    cout << "Nhập các phần tử của mảng: ";
    for (int i = 0; i < n; i++) {
        cin >> nums[i];
    }
    
    cout << "Nhập target: ";
    cin >> target;
    
    vector<vector<int>> pairs = twoSum(nums, target);
    
    if (pairs.empty()) {
        cout << "[]" << endl;
    } else {
        cout << "Các cặp chỉ số: ";
        for (const auto& p : pairs) {
            cout << "(" << p[0] << ", " << p[1] << ") ";
        }
        cout << endl;
    }
    
    return 0;
}