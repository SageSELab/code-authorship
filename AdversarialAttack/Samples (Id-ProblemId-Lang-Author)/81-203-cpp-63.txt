class Solution {
public:
    ListNode* removeElements(ListNode* head, int T) {
        if(!head) return nullptr;
        head -> next = removeElements(head -> next, T);
        return head -> val == T ? head -> next : head;
    }
};