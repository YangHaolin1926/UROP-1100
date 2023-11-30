from multiprocessing import Process, Queue
import pickle
import tarfile
import os
import re
from multiprocessing import Pool
from simhash import Simhash
import json
from datetime import datetime

width = 6
hash_k = 5
max_hash_len = 0

def get_features(s):
    s = s.lower()
    s = re.sub(r'[^\w]+', '', s)
    return [s[i:i + width] for i in range(max(len(s) - width + 1, 1))]

def book_index(num):
    hashes = []
    members = []
    print("Starting book_%0.3d"%(num), len(hashes))
    with open("split/book_%0.3d"%(num), "r") as f:
        lines = f.readlines()
        for idx, i in enumerate(lines):
            if idx % 200 == 0:
                print("This is book_%0.3d"%(num), idx)
            member = json.loads(i)
            try:
                if max_hash_len == 0:
                    hashes.append((str(idx + num * 2000), Simhash(get_features(member['text']))))
                else:
                    hashes.append((str(idx + num * 2000), Simhash(get_features(member['text'][:max_hash_len]))))
                members.append(member)
            except:
                continue
    print("Finishing book_%0.3d"%(num), len(hashes), len(members))
    return (hashes, members)

def get_book(njobs):
    with Pool(n_jobs) as p:
        hashes_members = p.map(book_index, [i for i in range(33)])
    return hashes_members 

def split_list(list, n):
    length = len(list)
    return [list[i*length // n: (i+1)*length // n] for i in range(n)]

def remove_duplicates(args):
    i, index = args
    unique_items = []
    for item in i:
        flag = 1
        try:
            now_list = index.get_near_dups(item[1])
            for x in now_list:
                if int(x) >= int(item[0]):
                    continue
                flag = 0
                break
            if flag == 1:
                unique_items.append(item)
        except:
            unique_items.append(item)
    return unique_items

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('-w', type=int, default=6, help='the window size')
    parser.add_argument('-k', type=int, default=5, help='find K nearest region')
    parser.add_argument('-l', type=int, default=0, help='the max length of the text for hashing, 0 means no limit')
    parser.add_argument('-n', type=int, default=100, help='the number of processes to run')

    args = parser.parse_args()

    width = args.w
    hash_k = args.k
    max_hash_len = args.l
    n_jobs = args.n

    outfile = "book2.jsonl"
    hashes_members = get_book(n_jobs)

    print("Finish getting hashes and members!")

    import itertools
    hashes = list(itertools.chain(*[item[0] for item in hashes_members]))

    import itertools
    members = list(itertools.chain(*[item[1] for item in hashes_members]))

    import re
    from simhash import Simhash, SimhashIndex

    index = SimhashIndex(hashes, k=hash_k)
    print("Finish building index!")

    from multiprocessing import Pool
    n_hashes = split_list(hashes, n_jobs)
    mem_hashes = list(zip(members, hashes))

    with Pool(n_jobs) as p:
        unique_hashes = p.map(remove_duplicates, [(i, index) for i in n_hashes])

    unique_hashes = list(itertools.chain(*unique_hashes))

    unique_mem_hashes = [(member, a_hash) for member, a_hash in mem_hashes if a_hash in unique_hashes]
    

    with open(outfile, 'w') as f:
        for mem, a_hash in unique_mem_hashes:
            meta = {}
            for feature in mem:
                if feature != "text":
                    meta[feature] = mem[feature]
            new = {"meta": meta, "text": mem["text"]}
            f.write(json.dumps(new) + '\n')
