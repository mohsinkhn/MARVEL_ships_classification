import argparse


if __name__=="__main__":
    parser = argparse.ArgumentParser("Prepare file with URLS for dowanloading")
    parser.add_argument("--input_file", type=str, default="VesselClassification.dat")
    parser.add_argument("--output_file", type=str, default="VesselClassificationURLS.dat")
    parser.add_argument("--image-size", type=str, default="small")
    args = parser.parse_args()

    with open(args.input_file, "r") as f:
        inp_data = f.read().split("\n")

    with open(args.output_file, "w") as f:
        err = 0
        for line in inp_data:
            try:
                imgid, flag, labelid, label = line.strip().split(",")
            except:
                print("Corrupt line")
                continue
            if len(imgid) >= 3:
                a, b, c = imgid[-1], imgid[-2], imgid[-3]
            elif len(imgid) == 2:
                a, b, c = imgid[-1], imgid[-2], imgid[-2]
            else:
                err += 1
                print("no data", imgid, err)
                continue

            url_path = "http://www.shipspotting.com/photos/{}/{}/{}/{}/{}.jpg".format(args.image_size, a, b, c, imgid)
            out_line = "{},{},{},{},{}\n".format(imgid, flag, labelid, label, url_path)
            f.write(out_line)

