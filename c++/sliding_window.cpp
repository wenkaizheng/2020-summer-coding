#include <iostream>
#include <vector>
#include <deque>
using namespace std;
class Solution {
public:
    vector<int> maxSlidingWindow(vector<int>& nums, int k) {
        vector<int> res;
        deque<int> q;
        for (int i = 0; i < nums.size(); ++i) {
            if (!q.empty() && q.front() == i - k) q.pop_front();
            while (!q.empty() && nums[q.back()] < nums[i]) q.pop_back();
            q.push_back(i);
            if (i >= k - 1) res.push_back(nums[q.front()]);
        }
        return res;
    }
};

class Solution1 {
public:
    int equalSubstring(string s, string t, int k) {
        int n = s.length(), i = 0, j;
        int diff[n];
        for (j = 0; j < n; ++j) {
            diff[j] = (s[j] - t[j]) >0? s[j] - t[j]: t[j]-s[j] ;
        }
        int start = 0;
        int rv = INT_MIN;
        int cost = 0;
        for (j = 0; j<n ; j++){
            cost += diff[j];
            while(cost >  k){
                cost -= diff[start];
                start ++;
            }
            rv = max(rv,j-start + 1);
        }
        //std::cout << i << std::endl;
        return rv;
    }
};

class Solution2 {
public:
    int minSubArrayLen(int s, vector<int>& nums)
    {
        int n = nums.size();
        int ans = INT_MAX;
        int left = 0;
        int sum = 0;
        for (int i = 0; i < n; i++) {
            sum += nums[i];
            while (sum >= s) {
                //  if(sum == s){
                ans = min(ans, i + 1 - left);
                //}
                sum -= nums[left];
                left ++;
            }
        }
        return (ans != INT_MAX ) ? ans : 0;
    }
};

int main(){
    vector<int> list2 {2,3,1,2,4,3};
    Solution2 s2;
    cout << s2.minSubArrayLen(7,list2) << endl;

    vector<int> list {1,3,-1,-3,5,3,6,7};
    Solution s;
    vector<int> rv = s.maxSlidingWindow(list,3);
    for (int& i : rv) {
        cout << i << endl;
    }

    Solution1 s1;
    string a = "abcde";
    string b = "bcdf";
    cout << s1.equalSubstring(a,b,3) <<endl;

}