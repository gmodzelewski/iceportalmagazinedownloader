package main

import (
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"path/filepath"
	"regexp"
	"strings"
	"time"

	"context"
	"github.com/chromedp/chromedp"
)

var magazineURLs = []string{
	"https://iceportal.de/zeitungskiosk/brand_eins",
	"https://iceportal.de/zeitungskiosk/brigitte",
	"https://iceportal.de/zeitungskiosk/capital",
	"https://iceportal.de/zeitungskiosk/cicero",
	"https://iceportal.de/zeitungskiosk/couch",
	"https://iceportal.de/zeitungskiosk/die_welt",
	"https://iceportal.de/zeitungskiosk/e_commerce_magazin",
	"https://iceportal.de/zeitungskiosk/falstaff",
	"https://iceportal.de/zeitungskiosk/fas",
	"https://iceportal.de/zeitungskiosk/faz",
	"https://iceportal.de/zeitungskiosk/flow",
	"https://iceportal.de/zeitungskiosk/geliebte_katze",
	"https://iceportal.de/zeitungskiosk/geo",
	"https://iceportal.de/zeitungskiosk/handelsblatt",
	"https://iceportal.de/zeitungskiosk/mens_health_de",
	"https://iceportal.de/zeitungskiosk/monopol",
	"https://iceportal.de/zeitungskiosk/psychologie_heute",
	"https://iceportal.de/zeitungskiosk/schoener_wohnen",
	"https://iceportal.de/zeitungskiosk/stern",
	"https://iceportal.de/zeitungskiosk/sueddeutsche_zeitung",
	"https://iceportal.de/zeitungskiosk/tagesspiegel",
	"https://iceportal.de/zeitungskiosk/taz_die_tageszeitung",
	"https://iceportal.de/zeitungskiosk/financial_times",
	"https://iceportal.de/zeitungskiosk/sports_illustrated",
	"https://iceportal.de/zeitungskiosk/the_london_standard",
}

func main() {
	downloadFolder := "downloaded_magazines"
	os.MkdirAll(downloadFolder, os.ModePerm)

	// Clean folder
	files, err := os.ReadDir(downloadFolder)
	if err != nil {
		log.Fatal(err)
	}
	for _, file := range files {
		os.Remove(filepath.Join(downloadFolder, file.Name()))
	}

	// Setup chromedp
	ctx, cancel := chromedp.NewContext(context.Background())
	defer cancel()

	for _, url := range magazineURLs {
		if err := downloadMagazine(ctx, url, downloadFolder); err != nil {
			log.Println("Error downloading magazine:", url, err)
		}
	}
}

func downloadMagazine(ctx context.Context, url, downloadFolder string) error {
	log.Println("Navigating to:", url)

	var downloadURL string

	err := chromedp.Run(ctx,
		chromedp.Navigate(url),
		chromedp.WaitVisible(`//span[contains(@class, "link-text") and (text()="Jetzt lesen" or text()="Read now")]`, chromedp.BySearch),
		chromedp.AttributeValue(`//span[contains(@class, "link-text") and (text()="Jetzt lesen" or text()="Read now")]/ancestor::a`, "href", &downloadURL, nil),
	)
	if err != nil {
		return fmt.Errorf("chromedp error: %v", err)
	}

	if downloadURL == "" {
		return fmt.Errorf("download URL not found")
	}

	// Add base URL if missing
	if !strings.HasPrefix(downloadURL, "http://") && !strings.HasPrefix(downloadURL, "https://") {
		downloadURL = "https://iceportal.de/" + strings.TrimLeft(downloadURL, "/")
	}

	log.Println("Downloading PDF from:", downloadURL)

	resp, err := http.Get(downloadURL)
	if err != nil {
		return err
	}

	if resp.StatusCode != http.StatusOK {
		resp.Body.Close()
		return fmt.Errorf("bad response: %s", resp.Status)
	}
	defer resp.Body.Close()

	currentDate := time.Now().Format("2006-01-02")
	filename := filepath.Join(downloadFolder, fmt.Sprintf("%s_%s.pdf", sanitizeFilename(url), currentDate))

	file, err := os.Create(filename)
	if err != nil {
		return err
	}
	defer file.Close()

	_, err = io.Copy(file, resp.Body)
	if err != nil {
		return err
	}

	log.Println("Successfully downloaded:", filename)
	return nil
}

func sanitizeFilename(url string) string {
	parts := strings.Split(strings.Trim(url, "/"), "/")
	name := parts[len(parts)-1]
	// Replace unwanted characters
	reg := regexp.MustCompile(`[\\/:*?"<>|]`)
	return reg.ReplaceAllString(name, "_")
}
