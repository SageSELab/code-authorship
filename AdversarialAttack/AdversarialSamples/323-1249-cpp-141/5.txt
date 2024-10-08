class SnapshotArray {
public:
   int snapNo=0;
   vector<map<int,int>> ar;

    SnapshotArray(int length) {
        ar.resize(length);
        for(int i=0;i<length;i++){
            ar[i][0]=0;
        }
    }
    
    void set(int index, int val) {
        
        ar[index][snapNo]=val;
    }
    
    int snap() {
        snapNo++;
        return snapNo-1;
    }
    
    int get(int index, int snap_id) {
    // we will check that if a given snap_id exists in a snapshot
    // ar[index] and returns the value associated with that snap_id
    //  if found. If the snap_id is not present, it returns the 
    //  closest value that is less than the snap_id from the
    //  previous snapshots.
      if(ar[index].find(snap_id)==ar[index].end()){

          auto i= --ar[index].lower_bound(snap_id);
          return i->second;
      }
        return ar[index][snap_id];
    }
};

/**
 * Your SnapshotArray object will be instantiated and called as such:
 * SnapshotArray* obj = new SnapshotArray(length);
 * obj->set(index,val);
 * int param_2 = obj->snap();
 * int param_3 = obj->get(index,snap_id);
 */