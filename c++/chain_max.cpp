#include <iostream>
#include<vector>
using namespace std;
class Solution {
public:
    
    int findLongestChain(vector<vector<int>>& pairs) {
      sort(pairs.begin(),pairs.end());
      //cout<<pairs[1][0] <<endl;
        vector<int>lis(pairs.size(),1);
        int ans= 1;
        for(int i=1;i<pairs.size();i++)
        {
            for(int j=0;j<i;j++)
            {
                if((pairs[i][0]>pairs[j][1])&&(lis[i]<=lis[j]))
                    lis[i]=1+lis[j];
                    ans = max(ans,lis[i]);
            }
        }
       
        return ans;
    }
};
int main(){
    Solution s =Solution();
    vector<vector<int>> vect1 = {
          {1,2},
          {2,3},
          {3,4},
    };
    cout << s.findLongestChain(vect1) <<endl;
}